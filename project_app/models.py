from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'
        ordering = ['name']


TYPES = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna'),
)


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.IntegerField(choices=TYPES, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.name} ({dict(TYPES).get(self.type, 'Nieznany rodzaj instytucji')})"

    class Meta:
        verbose_name = 'Instytucja'
        verbose_name_plural = 'Instytucje'
        ordering = ['name']


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Quantity: {self.quantity}, Institution: {self.institution}'

    class Meta:
        verbose_name = 'Darowizna'
        verbose_name_plural = 'Darowizny'
        ordering = ['institution']
