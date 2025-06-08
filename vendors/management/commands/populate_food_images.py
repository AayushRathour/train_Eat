import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from vendors.models import FoodItem

class Command(BaseCommand):
    help = 'Finds images in static/images and assigns them to FoodItems if they match by name.'

    def handle(self, *args, **options):
        image_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        
        if not os.path.isdir(image_dir):
            self.stdout.write(self.style.ERROR(f"Image directory not found at: {image_dir}"))
            return

        self.stdout.write(f"Scanning for images in {image_dir}...")
        
        food_items = FoodItem.objects.all()
        image_files = os.listdir(image_dir)
        
        for food in food_items:
            found_image = False
            for image_file in image_files:
                # Get the filename without the extension
                image_name, _ = os.path.splitext(image_file)
                
                # Check if the food name matches the image name (case-insensitive)
                if food.name.lower() == image_name.lower():
                    image_path = os.path.join(image_dir, image_file)
                    
                    with open(image_path, 'rb') as f:
                        django_file = File(f)
                        # This will overwrite the existing image if there is one
                        food.image.save(image_file, django_file, save=True)
                    
                    self.stdout.write(self.style.SUCCESS(f"Successfully assigned '{image_file}' to '{food.name}'."))
                    found_image = True
                    break
            
            if not found_image:
                self.stdout.write(self.style.WARNING(f"No matching image found for '{food.name}'."))

        self.stdout.write(self.style.SUCCESS("Image population script finished.")) 