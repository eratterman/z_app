from django.db import models
from django.utils import timezone


class Listing(models.Model):
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    apt_num = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    sq_ft = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_bathrooms = models.CharField(max_length=20)
    description = models.CharField(max_length=2000)
    cost = models.CharField(max_length=20)
    create_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'<Listing object id: {self.id} - address: {self.address1}>'


class Image(models.Model):
    file_path = models.CharField(max_length=250)
    listing_id = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='listing_id'
    )
    description = models.CharField(max_length=2000)
    create_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
