from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST

from .forms import ContactMessageForm, CustomDesignForm, SignUpForm
from .models import CustomDesign, Vehicle


def home(request):
    return render(request, "garage/home.html")


def cars(request):
    return render(
        request,
        "garage/cars.html",
        {"vehicles": Vehicle.objects.filter(category="car")},
    )


def bikes(request):
    return render(
        request,
        "garage/bikes.html",
        {"vehicles": Vehicle.objects.filter(category="bike")},
    )


def _modification(request, vehicle):
    if request.method == "POST":
        form = CustomDesignForm(request.POST, category=vehicle.category)
        if form.is_valid():
            if not request.user.is_authenticated:
                request.session["pending_design"] = {
                    "vehicle_id": vehicle.pk,
                    **form.cleaned_data,
                }
                request.session.modified = True
                messages.info(request, "Log in or create an account to save this design.")
                return redirect(f"{reverse('login')}?next={request.path}")

            design = form.save(commit=False)
            design.user = request.user
            design.vehicle = vehicle
            design.save()
            messages.success(request, "Your design has been saved to your account.")
            return redirect(request.path)
    else:
        form = CustomDesignForm(category=vehicle.category)

    return render(
        request,
        "garage/modification.html",
        {
            "vehicle": vehicle,
            "form": form,
            "category_label": vehicle.get_category_display(),
            "is_bike": vehicle.category == "bike",
        },
    )


def car_modification(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id, category="car")
    return _modification(request, vehicle)


def bike_modification(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id, category="bike")
    return _modification(request, vehicle)


def gallery(request):
    designs = CustomDesign.objects.select_related("user", "vehicle")[:12]
    return render(request, "garage/gallery.html", {"designs": designs})


def about(request):
    return render(request, "garage/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks, your message has been sent.")
            return redirect("contact")
    else:
        form = ContactMessageForm()
    return render(request, "garage/contact.html", {"form": form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your account is ready. Please log in.")
        return redirect("login")
    return render(request, "garage/signup.html", {"form": form})


def _save_pending_design(request, user):
    pending = request.session.pop("pending_design", None)
    if not pending:
        return
    vehicle_id = pending.pop("vehicle_id", None)
    vehicle = Vehicle.objects.filter(pk=vehicle_id).first()
    if vehicle is None:
        messages.error(request, "That vehicle is no longer available; please build the design again.")
        return
    form = CustomDesignForm(pending, category=vehicle.category)
    if not form.is_valid():
        messages.error(request, "Your saved selections were invalid. Please build the design again.")
        return
    design = form.save(commit=False)
    design.user = user
    design.vehicle = vehicle
    design.save()
    messages.success(request, "Your design has been saved to your account.")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    next_url = request.POST.get("next") or request.GET.get("next", "")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            _save_pending_design(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("home")
        messages.error(request, "Invalid username or password.")
    return render(request, "garage/login.html", {"next": next_url})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")
