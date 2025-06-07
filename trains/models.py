from django.db import models

# Create your models here.

class Station(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']

class Platform(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='platforms')
    number = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.station.name} - Platform {self.number}"

    class Meta:
        unique_together = ['station', 'number']

class Train(models.Model):
    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='source_trains')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_trains')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.number})"

class TrainRoute(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    sequence = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.train.name} - {self.station.name}"

    class Meta:
        ordering = ['sequence']
        unique_together = ['train', 'station']

class TrainLocation(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    current_station = models.ForeignKey(Station, on_delete=models.CASCADE)
    next_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='next_station')
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('ON_TIME', 'On Time'),
        ('DELAYED', 'Delayed'),
        ('ARRIVED', 'Arrived'),
        ('DEPARTED', 'Departed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.train.name} at {self.current_station.name}"

    class Meta:
        ordering = ['-updated_at']
