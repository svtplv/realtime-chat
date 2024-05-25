from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Profile


User = get_user_model()


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        widgets = {
            "image": forms.FileInput(),
            "displayname": forms.TextInput(
                attrs={"placeholder": "Add display name"}
            ),
            "info": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Add information"}
            ),
        }


class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]
