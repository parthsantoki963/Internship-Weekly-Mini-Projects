from django.contrib import admin
from .models import Job, JobSeeker, Application

# Register your models here.
admin.site.register(Job)
admin.site.register(JobSeeker)
admin.site.register(Application)