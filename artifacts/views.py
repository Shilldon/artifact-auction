from django.shortcuts import render
from .models import Artifact

# Create your views here.
def artifacts_list(request):
    artifacts = Artifact.objects.all()
    return render(request, "artifacts.html", {"artifacts_list": artifacts})
