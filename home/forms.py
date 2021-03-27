from django import forms
from home.models import AttractionReviews


class ReviewForm(forms.ModelForm):
    Title = forms.CharField(max_length=100, help_text="Title:")
    Rating = forms.IntegerField(max_value=5, min_value=1, help_text="Rating:")
    DateVisited = forms.DateField(help_text="Date Visited:")
    TimeTaken = forms.DurationField(help_text="How long did it take you to fully explore this attraction?")
    Comment = forms.CharField(max_length=1000, help_text="Description:")
    Picture = forms.ImageField(required=False, help_text="Upload Image")

    class Meta:
        model = AttractionReviews
        exclude = ("Likes", "AttractionReviewed", "UserReviewing", "DateAdded")
