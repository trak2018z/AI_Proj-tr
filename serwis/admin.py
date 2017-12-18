from django.contrib import admin
from serwis.models import *

# Register your models here.
admin.site.register(Profil)
admin.site.register(Friend)


class PostAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'data')


admin.site.register(Post, PostAdmin)
