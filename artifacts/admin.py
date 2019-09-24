from django.contrib import admin
from .models import Artifact, Category

# Register your models here.
admin.site.register(Artifact)
admin.site.register(Category)