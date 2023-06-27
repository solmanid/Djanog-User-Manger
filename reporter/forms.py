from django import forms

from reporter.models import PlacePoints


class CreatePointsForm(forms.ModelForm):
    # lat = forms.FloatField(widget=forms.TextInput(attrs={
    #     'type': 'hidden',
    #     # 'id': 'lat'
    # }))
    lng = forms.CharField(widget=forms.HiddenInput())
    lat = forms.CharField(widget=forms.HiddenInput())
    #
    # lng = forms.CharField()
    # lat = forms.CharField()

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
