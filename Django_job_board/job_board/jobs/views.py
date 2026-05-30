from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from .models import Job
from .serializers import JobSerializer, RegisterSerializer
from .tasks import send_job_alert_email

# ==========================================
# 1. THE JOB VIEWSET (Handles CRUD & Job Alert Emails)
# ==========================================
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        """Override create to trigger Celery task after a job is saved."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Get the saved job instance
        job = serializer.instance
        
        # TRIGGER THE CELERY TASK in the background
        send_job_alert_email.delay(job.id, job.title)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# ==========================================
# 2. THE REGISTRATION VIEW (Handles Signups)
# ==========================================
class RegisterView(generics.CreateAPIView):
    # AllowAny ensures anyone on the internet can access this endpoint to sign up
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer