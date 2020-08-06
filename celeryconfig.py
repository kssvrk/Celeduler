from kombu import Queue


broker_url = 'redis://192.168.0.13:6379/0'
task_default_queue = 'default'

# #------- django orm access---
# from django.conf import settings
# import django
# import os,sys
# dir_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(0,os.path.join(dir_path,'schadmin'))
# from schadmin.settings import DATABASES, INSTALLED_APPS
# settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
# django.setup()
# #-------------
from jobs.models import node

#---REGISTERING NODES AND THEIR QUEUES IN THE SCHEDULER-----
node_list=list(node.objects.all())
task_queues=[Queue('default')]
for node_element in node_list:
    task_queues.append(Queue(node_element.ip_address))

