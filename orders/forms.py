from django import forms
from .models import PNROrder

class PNROrderForm(forms.ModelForm):
    class Meta:
        model = PNROrder
        fields = ['pnr_number', 'train_number', 'train_name', 'from_station', 
                 'to_station', 'journey_date', 'class_type', 'passenger_count']
        widgets = {
            'journey_date': forms.DateInput(attrs={'type': 'date'}),
            'class_type': forms.Select(choices=[
                ('1A', 'First AC'),
                ('2A', 'Second AC'),
                ('3A', 'Third AC'),
                ('SL', 'Sleeper'),
                ('CC', 'Chair Car'),
                ('EC', 'Executive Class')
            ]),
        }

    def clean_pnr_number(self):
        pnr = self.cleaned_data.get('pnr_number')
        if not pnr.isdigit() or len(pnr) != 10:
            raise forms.ValidationError('PNR number must be 10 digits.')
        return pnr

class TrackOrderForm(forms.Form):
    order_number = forms.CharField(max_length=20, label="Order Number")

class CheckoutForm(forms.Form):
    pnr_number = forms.CharField(max_length=10, label="PNR Number")
    mobile_number = forms.CharField(max_length=15, label="Mobile Number")
    delivery_station_name = forms.CharField(max_length=100, label="Station of Food Delivery")
    special_instructions = forms.CharField(widget=forms.Textarea, required=False) 