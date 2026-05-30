from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import JobSeeker

# ==========================================
# TASK 1: THE JOB ALERT EMAIL
# ==========================================
@shared_task
def send_job_alert_email(job_id, job_title):
    """
    Finds all subscribed job seekers and sends them an email 
    alerting them of the new job post.
    """
    subscribers = JobSeeker.objects.filter(is_subscribed=True)
    
    if not subscribers.exists():
        return "No subscribers found."

    recipient_list = [seeker.user.email for seeker in subscribers if seeker.user.email]
    
    subject = f"New Job Alert: {job_title}"
    message = f"A new job '{job_title}' has just been posted! Check it out on the job board."
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    
    return f"Successfully sent {len(recipient_list)} alert emails."


# ==========================================
# TASK 2: THE WELCOME EMAIL
# ==========================================
@shared_task
def send_welcome_email(user_email, username):
    """Sends a welcome email to newly registered job seekers."""
    subject = "Welcome to the Job Board!"
    message = f"Hi {username},\n\nYou are successfully registered and subscribed to receive job alerts. We will email you the moment a new position is posted!"
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )
    
    return f"Welcome email sent to {user_email}"