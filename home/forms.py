from django import forms
from home.models import AttractionReviews
from django.forms.widgets import NumberInput
from durationwidget.widgets import TimeDurationWidget


class ReviewForm(forms.ModelForm):
    Title = forms.CharField(max_length=100)
    Rating = forms.IntegerField(max_value=5, min_value=1, help_text="Rating between 1-5")
    DateVisited = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label="Date visited")
    TimeTaken = forms.DurationField(widget=TimeDurationWidget(show_days=False, show_seconds=False), initial='0:0', label="Time taken to explore")
    Comment = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows':15}), label="More details")
    Picture = forms.ImageField(required=False, help_text="Upload an Image")

    class Meta:
        model = AttractionReviews
        exclude = ("Likes", "AttractionReviewed", "UserReviewing", "DateAdded")
