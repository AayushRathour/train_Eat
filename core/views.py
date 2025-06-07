from django.shortcuts import render
from vendors.models import FoodItem

def home(request):
    foods = FoodItem.objects.all()[:6]
    return render(request, 'core/home.html', {'foods': foods})

def about(request):
    """View for the about page."""
    return render(request, 'core/about.html')

def contact(request):
    """View for the contact page."""
    return render(request, 'core/contact.html')

def faq(request):
    """View for the FAQ page."""
    return render(request, 'core/faq.html')

def terms(request):
    """View for the Terms and Conditions page."""
    return render(request, 'core/terms.html')

def privacy(request):
    """View for the Privacy Policy page."""
    return render(request, 'core/privacy.html')

def refund(request):
    """View for the Refund Policy page."""
    return render(request, 'core/refund.html')

def help_center(request):
    """View for the Help Center page."""
    return render(request, 'core/help.html') 