from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, CustomDesign, Vehicle


class AutoCraftFlowTests(TestCase):
    def setUp(self):
        self.car = Vehicle.objects.create(
            category="car",
            company="BMW",
            name="M4 Competition",
            image_url="https://example.com/m4.jpg",
        )
        self.bike = Vehicle.objects.create(
            category="bike",
            company="KTM",
            name="390 Duke",
            image_url="https://example.com/duke.jpg",
        )
        self.user = User.objects.create_user(
            username="builder",
            email="builder@example.com",
            password="SecurePass!24",
        )

    def design_payload(self, *, bike=False):
        return {
            "name": "Weekend track build",
            "color": "#d92d20",
            "wheels": "track",
            "spoiler": "gt",
            "stickers": "stripes",
            "exhaust": "titanium",
            "accessories": ["lighting", "grips"] if bike else ["brakes", "lighting"],
        }

    def test_catalog_routes_are_separate_and_only_show_their_category(self):
        cars_response = self.client.get(reverse("cars"))
        bikes_response = self.client.get(reverse("bikes"))

        self.assertContains(cars_response, "BMW")
        self.assertNotContains(cars_response, "390 Duke")
        self.assertContains(bikes_response, "KTM")
        self.assertNotContains(bikes_response, "M4 Competition")
        self.assertEqual(
            self.client.get(reverse("car_modification", args=[self.bike.pk])).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(reverse("bike_modification", args=[self.car.pk])).status_code,
            404,
        )

    def test_customizer_keeps_the_vehicle_image_source_unchanged(self):
        path = reverse("car_modification", args=[self.car.pk])
        response = self.client.get(path)

        self.assertContains(response, 'src="https://example.com/m4.jpg"', html=False)
        self.assertContains(response, 'id="previewPaintSwatch"', html=False)
        self.assertNotContains(response, "preview-tint")

    def test_signup_saves_profile_and_hashes_password(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newbuilder",
                "first_name": "New",
                "last_name": "Builder",
                "email": "new@example.com",
                "password1": "StrongPass!783",
                "password2": "StrongPass!783",
            },
        )

        self.assertRedirects(response, reverse("login"))
        created = User.objects.get(username="newbuilder")
        self.assertEqual(created.email, "new@example.com")
        self.assertEqual(created.first_name, "New")
        self.assertNotEqual(created.password, "StrongPass!783")
        self.assertTrue(created.check_password("StrongPass!783"))

    def test_login_authenticates_registered_user(self):
        response = self.client.post(
            reverse("login"),
            {"username": "builder", "password": "SecurePass!24"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_saved_car_design_persists_every_selected_option(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("car_modification", args=[self.car.pk]), self.design_payload()
        )

        self.assertRedirects(response, reverse("car_modification", args=[self.car.pk]))
        design = CustomDesign.objects.get(user=self.user, vehicle=self.car)
        self.assertEqual(design.name, "Weekend track build")
        self.assertEqual(design.color, "#d92d20")
        self.assertEqual(design.wheels, "track")
        self.assertEqual(design.spoiler, "gt")
        self.assertEqual(design.stickers, "stripes")
        self.assertEqual(design.exhaust, "titanium")
        self.assertEqual(design.accessories, ["brakes", "lighting"])

    def test_guest_build_is_saved_after_login(self):
        path = reverse("bike_modification", args=[self.bike.pk])
        guest_response = self.client.post(path, self.design_payload(bike=True))
        self.assertRedirects(guest_response, f"{reverse('login')}?next={path}")
        self.assertIn("pending_design", self.client.session)

        login_response = self.client.post(
            reverse("login"),
            {
                "username": "builder",
                "password": "SecurePass!24",
                "next": path,
            },
        )
        self.assertRedirects(login_response, path)
        design = CustomDesign.objects.get(user=self.user, vehicle=self.bike)
        self.assertEqual(design.accessories, ["lighting", "grips"])
        self.assertEqual(design.exhaust, "titanium")
        self.assertNotIn("pending_design", self.client.session)

    def test_invalid_customization_is_not_saved(self):
        self.client.force_login(self.user)
        payload = self.design_payload()
        payload["color"] = "javascript:alert(1)"
        response = self.client.post(
            reverse("car_modification", args=[self.car.pk]), payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomDesign.objects.exists())

    def test_contact_form_persists_in_admin_managed_table(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "A Driver",
                "email": "driver@example.com",
                "message": "Please add a new vehicle.",
            },
        )
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertTrue(admin.site.is_registered(ContactMessage))

    def test_users_vehicles_and_designs_are_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(User))
        self.assertTrue(admin.site.is_registered(Vehicle))
        self.assertTrue(admin.site.is_registered(CustomDesign))
