# Django build-in
from django import forms

# Local Django
from reporter.models import PlacePoints


class CreatePointsForm(forms.ModelForm):
    lng = forms.CharField(widget=forms.HiddenInput())
    lat = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = PlacePoints
        fields = {
            # 'lat',
            # 'lng',
            'picture',
            'description',
        }

        widgets = {
            'picture': forms.FileInput(attrs={

                "class": " btn-success fileinput-button dz-clickable",
                "placeholder": "Picture",

            }),
            'description': forms.Textarea(attrs={

                # "class": "form-control",
                "placeholder": "Description",
            }),
        }
