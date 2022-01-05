from django.contrib import admin
from .models import Listing, Image


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'address1',
        'address2',
        'apt_num',
        'city',
        'state',
        'zip_code',
        'sq_ft',
        'num_bedrooms',
        'num_bathrooms',
        'description',
        'cost'
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file_path',
        'description',
        'listing_id'
    )
