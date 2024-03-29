from datetime import time

from django.db import models

from accounts.models import User
from accounts.utils import send_notification


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    # user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                email_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved:
                    # send email notification
                    mail_subject = "Your Restaurant is approved you are ready to roll"
                    send_notification(mail_subject, email_template, context)
                else:
                    # send notification email
                    mail_subject = "Sorry we are unable to work with your restaurant at this time"

                    send_notification(mail_subject, email_template, context)
        return super(Vendor, self).save(*args, **kwargs)


class OpeningHours(models.Model):
    days = [
        (1, 'saturday'),
        (2, 'sunday'),
        (3, 'monday'),
        (4, 'tuesday'),
        (5, 'wednesday'),
        (6, 'thursday'),
        (7, 'friday'),
    ]
    hours_of_day_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in
                       range(0, 60, 30)]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.SmallIntegerField(choices=days)
    from_hours = models.CharField(choices=hours_of_day_24, max_length=22, blank=True)
    to_hours = models.CharField(choices=hours_of_day_24, max_length=22, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', 'from_hours', 'to_hours')
        unique_together = ('vendor', 'day', 'from_hours', 'to_hours')

    def __str__(self):
        return self.get_day_display()
