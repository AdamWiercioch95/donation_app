from django.contrib import admin

from .models import Category, Institution, Donation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    list_filter = ('type', 'categories')
    search_fields = ('name', 'description')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'institution', 'address', 'phone_number', 'city', 'zip_code', 'pick_up_date')
    list_filter = ('institution', 'categories', 'pick_up_date')
    search_fields = ('address', 'city', 'phone_number')
