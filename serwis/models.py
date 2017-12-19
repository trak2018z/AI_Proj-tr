from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Profil(models.Model):
    PLCI = (
        ('M', 'Mężczyzna'),
        ('F', 'Kobieta'),
    )
    uzytkownik = models.OneToOneField(User, on_delete=models.CASCADE)
    lokacja = models.CharField(max_length=40, blank=True, null=True,)
    wiek = models.IntegerField(blank=True, null=True)
    plec = models.CharField(max_length=1, choices=PLCI, null=False, default='M')

    @receiver(post_save, sender=User)
    def update_profile(sender, instance, created, **kwargs):
        if created:
            Profil.objects.create(uzytkownik=instance)
        instance.profil.save()

    def __str__(self):
        return self.uzytkownik.username


class Post(models.Model):
    RODZAJ = (
        ('s', 'Śniadanie'),
        ('o', 'Obiad'),
        ('d', 'Deser'),
        ('k', 'Kolacja'),
        ('i', 'Inne'),
    )
    autor = models.ForeignKey(User)
    tytul = models.CharField(max_length=50, null=False, blank=False)
    data = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)
    podsumowanie = models.CharField(max_length=200)
    rodzaj = models.CharField(max_length=1, choices=RODZAJ, null=False, default='i')
    tresc = models.TextField()
    obraz = models.ImageField(upload_to='img', null=True, blank=True)


    class Meta:
        ordering = ['-data']

    def __str__(self):
        return self.tytul

    def get_absolute_url(self):
        return reverse('serwis.views.post', args=[self.slug])


class Friend(models.Model):
    friends = models.ManyToManyField(User, related_name='Lista_Znajomych')
    current_user = models.ForeignKey(User, related_name='Wlasciciel', null=True)


    @classmethod
    def dodawanie(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.friends.add(new_friend)

    @classmethod
    def usuwanie(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.friends.remove(new_friend)

    def __str__(self):
        return str(self.current_user)
