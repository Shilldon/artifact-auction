from django.shortcuts import render
from artifacts.models import Artifact

# Create your views here.
def search(request):
    artifacts_list = Artifact.objects.filter(description__icontains=request.GET['search'])
    return render(request, "artifacts.html", {"artifacts_list": artifacts_list})