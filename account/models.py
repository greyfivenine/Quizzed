from django.db import models
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.contrib.auth.models import User

import os

# Create your models here.

def generate_profile_filename(instance, filename):
    return 'profile_images/user_{0}/{1}'.format(instance.user.id, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=generate_profile_filename, blank=True, default='default.png')

    def __str__(self):
        return self.user.username

@receiver(pre_save, sender=UserProfile)
def person_data_pre_save(sender, instance, **kwargs):
    try:
        old_person_data = sender.objects.get(pk=instance.pk)
        if not old_person_data.picture == instance.picture:
            handle_user_image_delete(sender=sender, img_path=old_person_data.picture.path)
    except ObjectDoesNotExist as e:
        pass

def handle_user_image_delete(sender, **kwargs):
    img_path = kwargs.get('img_path')
    if os.path.exists(img_path):
        if not img_path.find('default.png') > 0:
            os.remove(img_path)
