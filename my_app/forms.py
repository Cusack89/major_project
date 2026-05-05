from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Injury

class InjuryForm(forms.ModelForm):
    class Meta:
        model = Injury
        fields = ["body_area", "pain_type", "severity", "date_occurred", "notes"]

        widgets = {
            "severity": forms.NumberInput(attrs={
                "min": 0,
                "max": 10,
                "required": True,
            }),
            "date_occurred": forms.DateInput(attrs={
                "type": "date",
                "required": True,
            }),
            "notes": forms.Textarea(attrs={
                "rows": 3,
            }),
        }

    def clean_severity(self):
        severity = self.cleaned_data.get("severity")

        if severity is None:
            raise forms.ValidationError("Severity is required.")

        if severity < 0 or severity > 10:
            raise forms.ValidationError("Severity must be between 0 and 10.")

        return severity

    def clean_date_occurred(self):
        date_occurred = self.cleaned_data.get("date_occurred")
        today = timezone.localdate()
        six_months_ago = today - timedelta(days=183)

        if date_occurred is None:
            raise forms.ValidationError("Date occurred is required.")

        if date_occurred > today:
            raise forms.ValidationError("Date cannot be in the future.")

        if date_occurred < six_months_ago:
            raise forms.ValidationError("Date cannot be more than 6 months ago.")

        return date_occurred