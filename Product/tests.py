from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from .models import Category, Brand, Product, Discount


class ProductModelTest(TestCase):

    def setUp(self) -> None:
        self.c1 = Category.objects.create(
            name='Electronic',
            slug='Electronic',
        )
        self.c2 = Category.objects.create(
            name='Phone',
            slug='Phone',
            parent=self.c1,
        )
        self.c3 = Category.objects.create(
            name='Computer',
            slug='Computer',
            parent=self.c1
        )
        self.c4 = Category.objects.create(
            name='Smart',
            slug='Smart',
            parent=self.c2
        )
        self.b1 = Brand.objects.create(
            name='Samsung'
        )
        self.b2 = Brand.objects.create(
            name='Apple'
        )
        self.d1 = Discount.objects.create(
            type='PT',
            discount_in_percent=20,
            maximum_amount=200000
        )
        self.d2 = Discount.objects.create(
            type='AM',
            discount_in_amount=20000,
        )
        self.p1 = Product.objects.create(
            name='S21',
            brand=self.b1,
            category=self.c4,
            inventory=20,
            price=45000000,
            discount=self.d1
        )
        self.p2 = Product.objects.create(
            name='12',
            brand=self.b2,
            category=self.c4,
            inventory=20,
            price=20000000,
            discount=self.d2
        )
        self.p3 = Product.objects.create(
            name='macbook',
            brand=self.b2,
            category=self.c4,
            inventory=20,
            price=56000000,
            discount=self.d2,
            deleted=True
        )

    def test1_category(self):
        self.assertIn(self.c2, Category.objects.all())

    def test2_category(self):
        self.assertIn(self.c2, Category.objects.filter(parent=self.c1))

    def test3_category(self):
        self.assertEqual(self.c4.parent.parent, self.c1)

    def test1_discount(self):
        self.d1 = Discount.objects.create(
            type='PT',
            discount_in_percent=20,
            maximum_amount=20000
        )

    def test2_discount(self):
        self.d1 = Discount.objects.create(
            type='AM',
            discount_in_amount=20000,
        )

    def test1_product(self):
        self.p1 = Product.objects.create(
            name='S21',
            brand=self.b1,
            category=self.c4,
            inventory=20,
            price=20000000,
            discount=self.d1
        )

    def test2_product(self):
        self.p1 = Product.objects.create(
            name='S21',
            brand=self.b1,
            category=self.c4,
            inventory=20,
            price=20000000,
            discount=self.d2
        )

    def test1_final_price(self):
        self.assertEqual(self.p1.final_price(), 19800000)

    def test2_final_price(self):
        d1 = Discount.objects.create(
            type='PT',
            discount_in_percent=5,
            maximum_amount=500000
        )

        p1 = Product.objects.create(
            name='S21',
            brand=self.b1,
            category=self.c4,
            inventory=20,
            price=2000000,
            discount=d1
        )
        self.assertEqual(p1.final_price(), 1900000)

    def test3_final_price(self):
        d = Discount.objects.create(
            type='AM',
            discount_in_amount=250000,
        )

        p1 = Product.objects.create(
            name='S21',
            brand=self.b1,
            category=self.c4,
            inventory=20,
            price=2000000,
            discount=d
        )
        self.assertEqual(p1.final_price(), 1750000)

    def test4_final_price(self):
        p1 = Product.objects.create(
            name='S21',
            brand=self.b1,
            category=self.c4,
            inventory=20,
            price=2000000,
        )
        self.assertEqual(p1.final_price(), 2000000)

    def test1_product_category_method(self):
        self.assertIn(self.p1, Product.filter_by_category(self.c4))

    def test2_product_deleted_category_method(self):
        self.assertNotIn(self.p3, Product.filter_by_category(self.c4))
