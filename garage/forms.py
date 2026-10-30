from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ContactMessage, CustomDesign


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class CustomDesignForm(forms.ModelForm):
    CAR_WHEELS = [
        ("stock", "Factory wheels"),
        ("street", "Street alloy wheels"),
        ("track", "Forged track wheels"),
        ("offroad", "All-terrain wheels"),
    ]
    BIKE_WHEELS = [
        ("stock", "Factory wheels"),
        ("street", "Sport alloy wheels"),
        ("track", "Lightweight race wheels"),
        ("offroad", "Adventure wheels"),
    ]
    CAR_SPOILERS = [
        ("none", "No spoiler"),
        ("sport", "Sport spoiler"),
        ("gt", "GT rear wing"),
        ("touring", "Touring aero kit"),
    ]
    BIKE_SPOILERS = [
        ("none", "Stock tail"),
        ("sport", "Tail tidy"),
        ("gt", "Race cowl"),
        ("touring", "Touring tail setup"),
    ]
    CAR_ACCESSORIES = [
        ("brakes", "Performance brakes"),
        ("lighting", "LED lighting"),
        ("interior", "Interior trim"),
        ("roof_rack", "Roof rack"),
    ]
    BIKE_ACCESSORIES = [
        ("crash_bars", "Crash bars"),
        ("lighting", "LED lighting"),
        ("luggage", "Luggage rack"),
        ("grips", "Heated grips"),
    ]

    accessories = forms.MultipleChoiceField(
        choices=(), required=False, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = CustomDesign
        fields = ("name", "color", "wheels", "spoiler", "stickers", "exhaust", "accessories")
        widgets = {
            "color": forms.Select(),
        }

    def __init__(self, *args, category="car", **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
        if category == "bike":
            self.fields["wheels"].choices = self.BIKE_WHEELS
            self.fields["spoiler"].choices = self.BIKE_SPOILERS
            self.fields["accessories"].choices = self.BIKE_ACCESSORIES
        else:
            self.fields["wheels"].choices = self.CAR_WHEELS
            self.fields["spoiler"].choices = self.CAR_SPOILERS
            self.fields["accessories"].choices = self.CAR_ACCESSORIES
        self.fields["name"].required = False
        self.fields["name"].widget.attrs.update({"placeholder": "e.g. Midnight track build"})


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "message")
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
