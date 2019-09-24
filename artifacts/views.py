from django.shortcuts import render, get_object_or_404
from .models import Artifact

# Create your views here.
""" Display list of all artifacts """
def artifacts_list(request):
    artifacts = Artifact.objects.all()
    return render(request, "artifacts.html", {"artifacts_list": artifacts})

""" Display a single artifact """
def display_artifact(request, id):
    artifact = get_object_or_404(Artifact, pk=id)
    return render(request,"display_artifact.html", {'artifact' : artifact})
