from celery import Celery
#------- django orm access---
from django.conf import settings
import django
import os,sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.join(dir_path,'schadmin'))
from schadmin.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()
#-------------
app = Celery('asyncprocessing')
app.config_from_object('celeryconfig')

 

#------------------------ give the jobs here --------------------
from jobslist.math_jobs import add
@app.task
def addition(argument_file):
    import json
    data={}
    try:
        with open(argument_file) as f:
            data = json.load(f)
            return add(data['number1'],data['number2'])
    except:
        print('Exception occured while processing the task.')
