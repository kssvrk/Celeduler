from django.contrib import admin

# Register your models here.
from .models import job,process,node
# Register your models here.
admin.site.register(job)
admin.site.register(process)
admin.site.register(node)