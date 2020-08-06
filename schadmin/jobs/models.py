from django.db import models


import os,sys
dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0,dir_path)


class process(models.Model):
    name=models.CharField(max_length=50,null=False,unique=True)
    added_by=models.CharField(max_length=50)
    description=models.TextField()
    ram_needed=models.IntegerField(null=False,blank=False)#ram needed in Bytes

    def __str__(self):
        return f"{self.name}_added_by_{self.added_by}"

class node(models.Model):
    ip_address = models.CharField(max_length=50,null=False,unique=True)
    active = models.BooleanField(default=True)
    processes = models.ManyToManyField(process,blank=True)
    total_ram=models.IntegerField(blank=False,null=False)#inbytes

    def __str__(self):
        return f"{self.ip_address}_queue"


class job(models.Model):
    STATUS_CHOICES =(
        ("started", "Job Started"),
        ("queued", "Job is Queued for processing"),
        ("error", "Job stopped because of error in processing"),
        ("internal_error", "Job stopped because of an internal error in the system"),
        ("finished", "Job is finished"),
        ('ingested','Job is recieved by system')
    )
    status=models.CharField(choices=STATUS_CHOICES,default='ingested',max_length=25,null=False)
    queue_time=models.DateTimeField(null=True,blank=True)
    ingest_time=models.DateTimeField(auto_now_add=True,null=True)
    start_time=models.DateTimeField(blank=True,null=True)
    end_time=models.DateTimeField(blank=True,null=True)
    job_arguments=models.CharField(max_length=250,null=False)
    username=models.CharField(max_length=50,null=False)
    
    queue=models.ForeignKey(
        'node',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    process=models.ForeignKey(
        'process',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        pname=process.objects.get(id=self.process.id).name
        return pname+'_by_'+self.username+'_at_'+self.ingest_time.strftime("%Y-%m-%d %H:%M:%S")







