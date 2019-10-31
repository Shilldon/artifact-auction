from django.shortcuts import render, reverse, redirect, get_object_or_404
from .forms import ReviewForm
from .models import Review
from artifacts.models import Artifact

def add_review(request, id):
    artifact = get_object_or_404(Artifact, pk=id)

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        print(review_form['rating'].value())
        if review_form.is_valid:
            try:
                review = get_object_or_404(Review, artifact=id)
                #review.rating = review_form['rating']
                review.rating = review_form['rating'].value()
                review.description = review_form['description'].value()
            except:
                review = Review(rating=review_form['rating'].value(), description=review_form['description'].value(), artifact=artifact, reviewer=request.user)
                
            review.save()
            return redirect(reverse('display_artifact', kwargs={'id':artifact.id}))
        else:
            print("not valid")
    else:
        try:
            review = get_object_or_404(Review, artifact=id)        
            review_form = ReviewForm(instance=review)
        except:
            review_form = ReviewForm()
    
        return render(request, "add_review.html", { "review_form" : review_form, "artifact" : artifact })

def delete_review(request, id):
    artifact = get_object_or_404(Artifact, pk=id)
    review = get_object_or_404(Review, artifact=artifact)
    review.delete()
    return redirect(reverse('display_artifact', kwargs={'id':artifact.id}))
    
        