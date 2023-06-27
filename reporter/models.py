# from location_field.models.spatial import LocationField

# from location_field.models.spatial import LocationField
# Create your models here.


from django.contrib.gis.db import models

from accounts.models import User


# Create your models here.

class PlacePoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, upload_to='upload/ed')
    description = models.TextField()
    location = models.PointField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Description:{self.description} - {self.created} - state:{self.status} "
