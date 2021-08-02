from django.test import TestCase

# Create your tests here.
from Core.models import BaseTest


class BaseModelTest(TestCase):
    
    def setUp(self) -> None:
        self.m1 = BaseTest.objects.create()

    def test1_all_deleted(self):
        
        self.m1.deleted = True
        self.m1.save()

        self.assertNotIn(self.m1, BaseTest.objects.all())

    def test2_filter_deleted(self):
        self.m1.deleted = True
        self.m1.save()

        self.assertNotIn(self.m1, BaseTest.objects.filter())

    def test3_get_deleted(self):
        self.m1.deleted = True
        self.m1.save()

        self.assertRaises(Exception, BaseTest.objects.get, id=1)

    def test4_archive(self):
        self.m1.deleted = True
        self.m1.save()

        self.assertIn(self.m1, BaseTest.objects.archive())
        self.assertNotIn(self.m1, BaseTest.objects.all())
