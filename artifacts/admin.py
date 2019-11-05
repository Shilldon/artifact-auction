from django.contrib import admin
from .models import Artifact, Category
from .forms import ArtifactRegistrationForm

class ArtifactAdmin(admin.ModelAdmin):

    form = ArtifactRegistrationForm

admin.site.register(Artifact, ArtifactAdmin)
admin.site.register(Category)