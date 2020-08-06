
# from django.conf import settings
# import django
# import os,sys
# #------- django orm access---
# dir_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(0,os.path.join(dir_path,'schadmin'))
# from schadmin.settings import DATABASES, INSTALLED_APPS
# settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
# django.setup()
# #-------------


#scheduler_loop
import tasks
from jobs.models import job,process,node
import requests
import datetime
import time 


def RamFilter(job_current):
    good_to_go_nodes=[]
    #--- RAM CHECK----
    #check all the running/to be run jobs in each queue and add their ram_needed values
    #then substract the occupied value with this value
    #do-not run multiple queues on a single node,queue name is the node identifier. Use concurrency instead.
    needed_ram=process.objects.get(id=job_current.process.id).ram_needed
    node_list=list(node.objects.all())
    #--------------------------
    ram_occupancy_factor=0.85
    #--------------------------
    for node_element in node_list:
        jobs_in_queue=list(job.objects.filter(queue=node_element.id,status='started')|job.objects.filter(queue=node_element.id,status='queued'))
        occupied_ram=0
        total_ram=node_element.total_ram
        for job_element in jobs_in_queue:
            ram=process.objects.get(id=job_element.process.id).ram_needed
            occupied_ram=occupied_ram+ram
        if(occupied_ram+needed_ram)<ram_occupancy_factor*total_ram:
            good_to_go_nodes.append(node_element)
    return good_to_go_nodes

def getBestNode(job_current):
    #first filter for resources
    #try to get the ram needed compared with all the nodes free ram and filter   
    ram_ok_nodes=RamFilter(job_current) 
    return ram_ok_nodes[0]
        
        
while(True):
    #check for pending jobs, and apply async them.
    pending=list(job.objects.filter(status='ingested')|job.objects.filter(status='internal_error'))
    print(f"found {len(pending)} pending jobs")
    for pending_job in pending:
        try:
            print(f'Scheduling job => {pending_job.id}')
            best_node=getBestNode(pending_job)
            pname=process.objects.get(id=pending_job.process.id)
            async_method = getattr(tasks, pname.name)
            print(pending_job.job_arguments)
            async_method.apply_async(args=[pending_job.job_arguments,],queue=best_node.ip_address)
            pending_job.queue=best_node
            pending_job.queue_time=datetime.datetime.now()
            pending_job.status='queued'
            pending_job.save()
        except Exception as e:
            print(f'error in scheduling job {pending_job}.id {e}')
    time.sleep(30)
