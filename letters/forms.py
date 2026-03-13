from django import forms
from .models import Letter
from django.utils import timezone
from datetime import timedelta


class LetterAddressForm(forms.ModelForm):
    send_to_self = forms.BooleanField(
        required=False, initial=False, label="Send to Self"
    )

    class Meta:
        model = Letter
        fields = [
            "sender_fullname",
            "sender_nickname",
            "sender_place",
            "sender_city",
            "sender_state",
            "sender_country",
            "sender_pincode",
            "receiver_fullname",
            "receiver_nickname",
            "receiver_place",
            "receiver_city",
            "receiver_state",
            "receiver_country",
            "receiver_pincode",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        self.fields["sender_country"].widget.attrs["readonly"] = True
        self.fields["receiver_country"].widget.attrs["readonly"] = True


class LetterContentForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = [
            "delivery_date",
            "content",
            "image",
            "caption",
        ]
        widgets = {
            "delivery_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "Write your letter here...",
                }
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "caption": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Max 300 characters for image caption",
                }
            ),
        }

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get("delivery_date")
        if delivery_date:
            min_date = timezone.now().date() + timedelta(days=21)
            if delivery_date < min_date:
                raise forms.ValidationError(
                    f"Delivery date must be at least 21 days from today (on or after {min_date})."
                )
        return delivery_date

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        caption = cleaned_data.get("caption")

        if image and not caption:
            self.add_error(
                "caption", "A caption is mandatory when an image is uploaded."
            )

        return cleaned_data
