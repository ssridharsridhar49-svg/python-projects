from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cars/", views.cars, name="cars"),
    path("bikes/", views.bikes, name="bikes"),
    path("cars/<int:vehicle_id>/modify/", views.car_modification, name="car_modification"),
    path("bikes/<int:vehicle_id>/modify/", views.bike_modification, name="bike_modification"),
    path("gallery/", views.gallery, name="gallery"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
