from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from trains.models import Station, Platform

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
            )
        ]
    )
    email = models.EmailField()
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} at {self.station.name} - Platform {self.platform.number}"

    class Meta:
        ordering = ['name']
        unique_together = ['station', 'platform', 'name']

class FoodCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Food Categories'
        ordering = ['name']

class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='food_items')
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    image = models.ImageField(
        upload_to='food_images/',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_-]+\.(jpg|jpeg|png|gif)$',
                message=_("Only jpg, jpeg, png and gif files are allowed.")
            )
        ],
        blank=True,
        null=True
    )
    is_vegetarian = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    preparation_time = models.IntegerField(
        help_text='Preparation time in minutes',
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.vendor.name}"

    class Meta:
        ordering = ['name']
        unique_together = ['vendor', 'name']

class Review(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        validators=[MinValueValidator(1), MinValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.food_item.name} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['food_item', 'user']
