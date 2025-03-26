from django.db import models
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings

class Notice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    posted_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="notices")
    campus = models.ForeignKey('campus.Campus', on_delete=models.CASCADE, related_name="notices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    file_attachment = models.FileField(upload_to="notices/", null=True, blank=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        if is_new and self.status == 'published':
            self.send_notice_email()

    def send_notice_email(self):
        """
        Sends an email to all users of the campus when a new notice is published.
        """
        from users.models import CustomUser

        users = CustomUser.objects.filter(campus=self.campus, is_active=True)

        recipient_list = [user.email for user in users if user.email]

        if recipient_list:
            subject = f"New Notice: {self.title}"
            message = f"""
            Hello,

            A new notice has been posted for your campus: {self.campus.name}.

            Title: {self.title}
            Priority: {self.get_priority_display()}
            Description: {self.description}

            Please check the system for more details.

            Regards,
            Administration Team
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"