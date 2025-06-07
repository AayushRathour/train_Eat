import random
from django.core.management.base import BaseCommand
from vendors.models import Vendor, FoodCategory, FoodItem
from trains.models import Station, Platform

class Command(BaseCommand):
    help = 'Adds and categorizes Indian food items to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating and categorizing Indian food items...')

        # Get or create a station and platform
        station, _ = Station.objects.get_or_create(name='Main Station', code='MAIN')
        platform, _ = Platform.objects.get_or_create(station=station, number='1')

        # Get or create a vendor
        vendor, _ = Vendor.objects.get_or_create(
            name='Indian Delights',
            defaults={
                'owner_name': 'Ravi Kumar',
                'phone_number': '9876543210',
                'email': 'indian.delights@example.com',
                'station': station,
                'platform': platform,
                'description': 'Authentic Indian cuisine for your journey.',
            }
        )
        self.stdout.write(f'Using vendor: {vendor.name}')

        # Define categories
        categories = {
            "North Indian": "Rich and creamy curries, grilled meats and flatbreads.",
            "South Indian": "Lighter fare with an emphasis on rice, lentils, and stews.",
            "Desserts": "Sweet treats to complete your meal.",
            "Snacks": "Appetizers and small bites."
        }

        for cat_name, cat_desc in categories.items():
            category, created = FoodCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': cat_desc}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Food items with new categories
        food_items_data = [
            # North Indian
            {'name': 'Butter Chicken', 'cat': 'North Indian', 'desc': 'Tender chicken in a creamy tomato sauce.', 'price': 250.00, 'is_veg': False, 'img': 'food_items/butter_chicken.jpg'},
            {'name': 'Palak Paneer', 'cat': 'North Indian', 'desc': 'Creamed spinach with fresh paneer cheese.', 'price': 220.00, 'is_veg': True, 'img': 'food_items/palak_paneer.jpg'},
            {'name': 'Naan', 'cat': 'North Indian', 'desc': 'Soft and fluffy Indian bread.', 'price': 40.00, 'is_veg': True, 'img': 'food_items/naan.jpg'},
            {'name': 'Dal Makhani', 'cat': 'North Indian', 'desc': 'Creamy black lentils cooked overnight.', 'price': 180.00, 'is_veg': True, 'img': 'food_items/dal_makhani.jpg'},
            {'name': 'Chicken Biryani', 'cat': 'North Indian', 'desc': 'Aromatic basmati rice with spiced chicken.', 'price': 280.00, 'is_veg': False, 'img': 'food_items/biryani.jpg'},

            # South Indian
            {'name': 'Masala Dosa', 'cat': 'South Indian', 'desc': 'A crisp and savory pancake with a spiced potato filling.', 'price': 150.00, 'is_veg': True, 'img': 'food_items/masala_dosa.jpg'},
            {'name': 'Idli Sambar', 'cat': 'South Indian', 'desc': 'Steamed rice cakes served with a lentil-based vegetable stew.', 'price': 120.00, 'is_veg': True, 'img': 'food_items/idli_sambar.jpg'},
            {'name': 'Vada', 'cat': 'South Indian', 'desc': 'A savory fried snack made from black lentils.', 'price': 80.00, 'is_veg': True, 'img': 'food_items/vada.jpg'},

            # Snacks
            {'name': 'Samosa', 'cat': 'Snacks', 'desc': 'Crispy pastry filled with spiced potatoes and peas.', 'price': 30.00, 'is_veg': True, 'img': 'food_items/samosa.jpg'},
            {'name': 'Pakora', 'cat': 'Snacks', 'desc': 'Assorted vegetables dipped in gram flour batter and deep-fried.', 'price': 100.00, 'is_veg': True, 'img': 'food_items/pakora.jpg'},

            # Desserts
            {'name': 'Gulab Jamun', 'cat': 'Desserts', 'desc': 'Soft, spongy balls made of milk solids, soaked in sweet syrup.', 'price': 90.00, 'is_veg': True, 'img': 'food_items/gulab_jamun.jpg'},
            {'name': 'Jalebi', 'cat': 'Desserts', 'desc': 'A spiral-shaped sweet made from deep-fried batter, soaked in syrup.', 'price': 70.00, 'is_veg': True, 'img': 'food_items/jalebi.jpg'},
        ]

        for food_data in food_items_data:
            category = FoodCategory.objects.get(name=food_data['cat'])
            food_item, created = FoodItem.objects.update_or_create(
                name=food_data['name'],
                vendor=vendor,
                defaults={
                    'category': category,
                    'description': food_data['desc'],
                    'price': food_data['price'],
                    'image': food_data['img'],
                    'is_vegetarian': food_data['is_veg'],
                    'preparation_time': random.randint(15, 45)
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added {food_item.name} in {category.name}'))
            else:
                self.stdout.write(f'Updated {food_item.name} in {category.name}')

        # Delete the old 'Indian' category if it exists and is empty
        try:
            old_category = FoodCategory.objects.get(name='Indian')
            if not old_category.fooditem_set.exists():
                old_category.delete()
                self.stdout.write(self.style.SUCCESS('Deleted old "Indian" category.'))
        except FoodCategory.DoesNotExist:
            pass
            
        self.stdout.write(self.style.SUCCESS('Finished processing food items.')) 