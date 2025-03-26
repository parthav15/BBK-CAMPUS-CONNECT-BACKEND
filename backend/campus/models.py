from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class Campus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True, default="")
    city = models.CharField(max_length=100, null=True, blank=True, default="")
    state = models.CharField(max_length=100, null=True, blank=True, default="")
    country = models.CharField(max_length=100, null=True, blank=True, default="")
    zip_code = models.CharField(max_length=20, null=True, blank=True, default="")
    phone = models.CharField(max_length=20, null=True, blank=True, default="")
    email = models.EmailField(max_length=100, null=True, blank=True, default="")
    website = models.URLField(max_length=200, null=True, blank=True, default="")
    head_name = models.CharField(max_length=100, null=True, blank=True, default="")
    head_phone = models.CharField(max_length=20, null=True, blank=True, default="")
    head_email = models.EmailField(max_length=100, null=True, blank=True, default="")
    image = models.ImageField(upload_to='campus/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True, default="")
    established_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Incident(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]
    INCIDENT_TYPES = [
        ('theft', 'Theft'),
        ('harassment', 'Harassment'),
        ('accident', 'Accident'),
        ('fire', 'Fire'),
        ('vandalism', 'Vandalism'),
        ('medical', 'Medical Emergency'),
        ('natural_disaster', 'Natural Disaster'),
        ('lost_item', 'Lost Item'),
        ('stolen_item', 'Stolen Item'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    reported_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="incidents")
    campus = models.ForeignKey('campus.Campus', on_delete=models.CASCADE, related_name="incidents")
    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    media_files = models.JSONField(default=list, blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.send_incident_email()

    def send_incident_email(self):
        """
        Sends an email to the campus head when a new incident is reported.
        """
        if self.campus.head_email:
            subject = f"New Incident Reported: {self.title}"
            message = f"""
            Dear {self.campus.head_name},

            A new incident has been reported at {self.campus.name}.

            Incident Type: {self.get_incident_type_display()}
            Status: {self.get_status_display()}
            Location: {self.location if self.location else 'Not specified'}
            Reported By: {self.reported_by.get_full_name()} ({self.reported_by.email})

            Description:
            {self.description}

            Please take the necessary actions.

            Regards,
            Incident Management System
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.campus.head_email],
                fail_silently=False,
            )

    def __str__(self):
        return f"{self.title} - {self.get_status_display()} - {self.campus.name}"