from django import forms
from django.db.models import fields

from .models import Rating, RatingStar, Reviews

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):

    # asagidaki queryset data base-den butun ulduzlari goturub radioselect kimi teqdim edir
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)