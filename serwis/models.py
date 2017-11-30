from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Profil(models.Model):
    uzytkownik = models.OneToOneField(User, on_delete=models.CASCADE)
    lokacja = models.CharField(max_length=40, blank=True, null=True)
    data_ur = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def update_profile(sender, instance, created, **kwargs):
        if created:
            Profil.objects.create(uzytkownik=instance)
        instance.profil.save()

    def __str__(self):
        return self.uzytkownik.username
