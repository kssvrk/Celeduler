from kombu import Queue


broker_url = 'redis://192.168.0.13:6379/0'
task_default_queue = 'default'

from jobs.models import node

#---REGISTERING NODES AND THEIR QUEUES IN THE SCHEDULER-----
node_list=list(node.objects.all())
task_queues=[Queue('default')]
for node_element in node_list:
    task_queues.append(Queue(node_element.ip_address))

