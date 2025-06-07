from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vendor, FoodItem, FoodCategory
from django.db.models import Q

def vendor_list(request):
    """View to display a list of all vendors."""
    vendors = Vendor.objects.all()
    return render(request, 'vendors/vendor_list.html', {
        'vendors': vendors
    })

def vendor_detail(request, vendor_id):
    """View to display details of a specific vendor and their food items."""
    vendor = get_object_or_404(Vendor, id=vendor_id)
    food_items = vendor.food_items.filter(is_available=True).select_related('category')
    return render(request, 'vendors/vendor_detail.html', {
        'vendor': vendor,
        'food_items': food_items,
    })

def vendor_menu(request, vendor_id):
    """View to display the menu of a specific vendor."""
    vendor = get_object_or_404(Vendor, id=vendor_id)
    categories = FoodCategory.objects.filter(food_items__vendor=vendor).distinct()
    return render(request, 'vendors/vendor_menu.html', {
        'vendor': vendor,
        'categories': categories
    })

def vendor_reviews(request, vendor_id):
    """View to display reviews for a specific vendor."""
    vendor = get_object_or_404(Vendor, id=vendor_id)
    return render(request, 'vendors/vendor_reviews.html', {
        'vendor': vendor
    })

def food_detail(request, food_id):
    """View to display details of a specific food item."""
    food = get_object_or_404(FoodItem, id=food_id)
    return render(request, 'vendors/food_detail.html', {
        'food': food
    })

def category_list(request):
    """View to display all food categories."""
    categories = FoodCategory.objects.all()
    return render(request, 'vendors/category_list.html', {
        'categories': categories
    })

def category_detail(request, category_id):
    """View to display food items in a specific category."""
    category = get_object_or_404(FoodCategory, id=category_id)
    return render(request, 'vendors/category_detail.html', {
        'category': category
    })

def food_list(request):
    """View to display a list of all food items, grouped by category."""
    categories = FoodCategory.objects.prefetch_related('fooditem_set').all()
    food_by_category = {category: category.fooditem_set.all() for category in categories if category.fooditem_set.exists()}
    
    return render(request, 'vendors/food_list.html', {
        'food_by_category': food_by_category
    })

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = FoodItem.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(vendor__name__icontains=query)
        ).distinct()
    
    return render(request, 'vendors/search_results.html', {
        'query': query,
        'results': results
    })
