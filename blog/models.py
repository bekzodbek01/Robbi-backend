from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.timezone import localtime, now


class Region(models.Model):
    title = models.CharField(max_length=255, verbose_name="Region Name")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"


class City(models.Model):
    title = models.CharField(max_length=255, verbose_name="City Name")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Category(models.Model):
    name = models.CharField(max_length=255,  blank=True, null=True)
    image = models.FileField(upload_to='category', blank=True, null=True)
    icon_background_color = models.CharField(max_length=60, blank=True, null=True)
    icon_background_color_night = models.CharField(max_length=60, blank=True, null=True)
    Ln_background_color = models.CharField(max_length=60, blank=True, null=True)
    Ln_background_color_night = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class RestaurantFilter(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restaurant Filter"
        verbose_name_plural = "Restaurant Filters"


class KalinkaFilter(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kalinka Filter"
        verbose_name_plural = "Kalinka Filters"


class ParkFilter(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Park Filter"
        verbose_name_plural = "Park Filters"


from smart_selects.db_fields import ChainedForeignKey


class General(models.Model):
    TIER_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('standard', 'Standard'),
    ]

    STAR_RATINGS = (
        (5, '5 yulduzli'),
        (4, '4 yulduzli'),
        (3, '3 yulduzli'),
        (2, '2 yulduzli'),
    )

    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    city = ChainedForeignKey(
        City,
        chained_field="region",
        chained_model_field="region",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)
    rest_filter = models.ManyToManyField(RestaurantFilter, blank=True, related_name='restaurants')
    kalinka_filter = models.ForeignKey(KalinkaFilter, on_delete=models.SET_NULL, blank=True, null=True, related_name='kalinka')
    park_filter = models.ForeignKey(ParkFilter, on_delete=models.SET_NULL, blank=True, null=True, related_name='parks')
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, blank=True, null=True)
    delivery_available = models.BooleanField(default=False)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, blank=True, null=True)
    star_rating = models.PositiveSmallIntegerField(choices=STAR_RATINGS, blank=True, null=True, verbose_name="Yulduzlar soni")

    def __str__(self):
        return self.name or "No name"

    class Meta:
        verbose_name = "General Place"
        verbose_name_plural = "General Places"


class Helper(models.Model):
    general = models.OneToOneField(General, on_delete=models.CASCADE, related_name='helper')
    phone = models.CharField(max_length=50, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True, verbose_name='Latitude')
    long = models.FloatField(blank=True, null=True, verbose_name='Longitude')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.general)

    class Meta:
        verbose_name = "Helper"
        verbose_name_plural = "Helper"


class GeneralImage(models.Model):
    general = models.ForeignKey(General, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='general_images/', blank=True, null=True)


class MenuCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name or 'No name'

    class Meta:
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"


class MenuItem(models.Model):
    general = models.ForeignKey(General, on_delete=models.CASCADE, related_name='menu_items', blank=True, null=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    def __str__(self):
        return self.name or 'No name'

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
