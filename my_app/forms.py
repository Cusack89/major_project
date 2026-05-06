from django import forms
from .models import Injury

class InjuryForm(forms.ModelForm):
    PAIN_TYPES = [
        ("sharp", "Sharp"),
        ("dull", "Dull"),
        ("aching", "Aching"),
        ("burning", "Burning"),
        ("stiffness", "Stiffness"),
        ("cramping", "Cramping"),
        ("swelling", "Swelling"),
        ("other", "Other"),
    ]

    type_of_pain = forms.ChoiceField(choices=PAIN_TYPES)

    pain_level = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            "type": "range",
            "min": "1",
            "max": "10",
            "value": "5",
            "class": "pain-slider"
        })
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date"
        })
    )

    class Meta:
        model = Injury
        fields = [
            "location",
            "type_of_pain",
            "pain_level",
            "date",
            "notes",
        ]

        widgets = {
            "location": forms.HiddenInput(),
            "notes": forms.Textarea(attrs={
                "placeholder": "Add any extra details...",
                "rows": 5
            }),
        }