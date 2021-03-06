from django.shortcuts import render, reverse, redirect, get_object_or_404
from .forms import ReviewForm
from .models import Review
from artifacts.models import Artifact


def add_review(request, id):
    """
    A view to create a review instance an render view form for editing/adding
    review
    """
    artifact = get_object_or_404(Artifact, pk=id)

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid:
            """
            Try updating existing instance of review, if none, create a new
            review
            """
            try:
                review = get_object_or_404(Review, artifact=id)
                review.rating = review_form['rating'].value()
                review.description = review_form['description'].value()
            except:
                review = Review(rating=review_form['rating'].value(),
                                description=review_form['description'].value(),
                                artifact=artifact,
                                reviewer=request.user)

            review.save()
            return redirect(reverse('display_artifact',
                                    kwargs={'id': artifact.id}))
    else:
        try:
            review = get_object_or_404(Review, artifact=id)
            review_form = ReviewForm(instance=review)
        except:
            review_form = ReviewForm()

        return render(request,
                      "add_review.html",
                      {"review_form": review_form,
                       "artifact": artifact
                       }
                      )


def delete_review(request, id):
    """
    A view to delete an existing review
    """
    artifact = get_object_or_404(Artifact, pk=id)
    review = get_object_or_404(Review, artifact=artifact)
    review.delete()
    return redirect(reverse('display_artifact', kwargs={'id': artifact.id}))
