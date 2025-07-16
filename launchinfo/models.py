from django.db import models # type: ignore
from django.utils import timezone # type: ignore
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import os
import uuid

from waterinfo.models import Water
from kayakutils.models import Country, State, County, City
    
def generate_unique_launch_name(instance, filename):
    # Generate a unique filename using UUID and preserve the extension
    ext = filename.split('.')[-1]  # Get the file extension
    unique_name = f'{uuid.uuid4().hex}.{ext}'
    return os.path.join('launches', unique_name)

class Launch(models.Model):
    """
    Describes a boat launch (location, facilities, etc)
    """
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    body_of_water = models.ForeignKey(Water, on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    main_image = models.ForeignKey('launchinfo.LaunchImage', on_delete=models.SET_NULL, null=True, related_name="launch_main_image")

    BATHROOM_CHOICES = [
        (0, "None"),            # no bathrooms
        (1, "Outhouse"),        # outhouse/pit
        (2, "Plumbed"),         # running water
        (3, "Nearby"),          # neaby bathroom (convenience store, campground, etc)
    ]
    bathroom_type = models.SmallIntegerField(choices=BATHROOM_CHOICES, default=0)
    bathrooms = models.SmallIntegerField(default=0) # number of bathrooms/stalls
    bathroom_desc = models.TextField(null=True, blank=True) # short description, optional

    RampType = [
        (0, "None"),             # this shouldn't be needed, but just in case
        (1, "Hard Surfaced"),    # paved ramp
        (2, "Carry Down"),       # no ramp, but can carry boat to water
        (3, "Gravel"),           # gravel ramp
    ]
    ramp_type = models.SmallIntegerField(choices=RampType, default=1)

    ParkingType = [
        (0, "None"),             # no parking available
        (1, "Gravel"),           # gravel/dirt parking lot
        (2, "Paved"),            # paved parking lot
    ]
    parking_type = models.SmallIntegerField(choices=ParkingType, default=1)
    pay_parking = models.BooleanField(default=False)            # if payment is required to park
    pay_info = models.TextField(null=True, blank=True)    # payment details, if needed

    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class LaunchImage(models.Model):
    original = models.ImageField(upload_to=generate_unique_launch_name)
    thumbnail = ImageSpecField(source='original', processors=[ResizeToFit(200, 200)], format='JPEG', options={'quality': 60})
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    caption = models.CharField(max_length=256, null=True, blank=True)  # optional caption for the image

    def save(self, *args, **kwargs):
        # Automatically set the launch's main image if this is the first image
        if not self.launch.main_image:
            self.launch.main_image = self
            self.launch.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # If this image is the main image for the launch, set main_image to None
        if self.launch.main_image == self:
            self.launch.main_image = None
            self.launch.save()
        super().delete(*args, **kwargs)

    @property
    def image_url(self):
        return self.original.url if self.original else None

    @property
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else None

    @property
    def image_filename(self):
        return os.path.basename(self.original.name) if self.original else None

    @property
    def thumbnail_filename(self):
        return os.path.basename(self.thumbnail.name) if self.thumbnail else None

    @property
    def image_extension(self):
        return os.path.splitext(self.original.name)[1] if self.original else None

    @property
    def thumbnail_extension(self):
        return os.path.splitext(self.thumbnail.name)[1] if self.thumbnail else None

    @property
    def image_size(self):
        return self.original.size if self.original else None

    @property
    def thumbnail_size(self):
        return self.thumbnail.size if self.thumbnail else None

    @property
    def image_dimensions(self):
        return self.original.width, self.original.height if self.original else (None, None)

    @property
    def thumbnail_dimensions(self):
        return self.thumbnail.width, self.thumbnail.height if self.thumbnail else (None, None)

    @property
    def image_mime_type(self):
        return self.original.file.content_type if self.original else None

    @property
    def thumbnail_mime_type(self):
        return self.thumbnail.file.content_type if self.thumbnail else None

    @property
    def image_size_kb(self):
        return self.original.size / 1024 if self.original else None

    @property
    def thumbnail_size_kb(self):
        return self.thumbnail.size / 1024 if self.thumbnail else None

    @property
    def image_size_mb(self):
        return self.original.size / (1024 * 1024) if self.original else None

    @property
    def thumbnail_size_mb(self):
        return self.thumbnail.size / (1024 * 1024) if self.thumbnail else None

    @property
    def image_path(self):
        return self.original.path if self.original else None

    @property
    def thumbnail_path(self):
        return self.thumbnail.path if self.thumbnail else None

    @property
    def image_exists(self):
        return os.path.exists(self.image_path) if self.image_path else False

    @property
    def thumbnail_exists(self):
        return os.path.exists(self.thumbnail_path) if self.thumbnail_path else False

    @property
    def image_is_valid(self):
        return self.image_exists and self.image_mime_type.startswith('image/') if self.image_exists else False

    @property
    def thumbnail_is_valid(self):
        return self.thumbnail_exists and self.thumbnail_mime_type.startswith('image/') if self.thumbnail_exists else False

    def __str__(self):
        return f"Image {self.id} for Launch {self.launch.name}" if self.launch else f"Image {self.id}"