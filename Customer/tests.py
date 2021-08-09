from django.test import TestCase

# Create your tests here.
from .models import Customer, Address, User


class CustomerModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            first_name="Akbar",
            last_name="Akbari",
            phone="09163225566",
            email="akbar@gmail.com",
            password="12345"
        )
        self.customer = Customer.objects.create(
            user=self.user
        )
        self.address = Address.objects.create(
            owner=self.customer,
            province="Khouzestan",
            city="Mahshahr",
            exact_address="faz2-roshdiye",
            house_number=1,
            zip_code=123456
        )

    def test_create_user(self):
        self.user1 = User.objects.create(
            first_name="Hossein",
            last_name="Akbari",
            phone="09163226666",
            email="akr@gmail.com",
            password="12345"
        )
        self.customer = Customer.objects.create(
            user=self.user1
        )
        print(self.customer)
        self.assertEqual(self.user1.is_staff, False)

    def test_create_address(self):
        self.address = Address.objects.create(
            owner=self.customer,
            province="Khouzestan",
            city="Mahshahr",
            exact_address="faz2-roshdiye",
            house_number=1,
            zip_code=123456
        )
        print(self.address.owner)

    def test_filter_owner(self):
        self.assertIn(self.address, Address.filter_by_owner(self.customer))

    def test_filter_country(self):
        self.assertIn(self.address, Address.filter_by_country("Iran"))

    def test_filter_province(self):
        self.assertIn(self.address, Address.filter_by_province("Khouzestan"))

    def test_filter_city(self):
        self.assertIn(self.address, Address.filter_by_city("Mahshahr"))
