from myapp1.models import bookingData, packages, packagebookingData
from django import forms
from django.forms.widgets import TextInput


class BookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'single-input'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    AvailbleCapacity = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                       label="Available Capacity")
    Price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="Ticket Price(CAD)")
    TotalPrice = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="Total Price")

    class Meta:
        model = bookingData
        fields = ['user', 'aid', 'AvailbleCapacity', 'Price', 'People', 'TotalPrice', 'day', 'time', 'Comments']
        labels = {'user': 'User', 'aid': 'Adventure', 'AvailbleCapacity': 'Available Capacity',
                  'Price': 'Ticket Price(CAD)', 'People': 'People', 'TotalPrice': 'Total Price',
                  'day': 'Day of Booking', 'time': 'Slot of Booking Day', 'Comments': 'Comments'}


class PacakgesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'single-input'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    # AvailbleCapacity = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # Price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # TotalPrice = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = packages
        fields = ['package_name', 'package_activities', 'description', 'price', 'capacity', 'day']

        labels = {'package_name': 'Package', 'package_activities': 'Package Activities', 'description': 'Description',
                  'Price': 'Ticket Price(CAD)', 'capacity': 'Capacity',
                  'day': 'Day of Booking'}


class BookPacakgesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'single-input'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    AvailbleCapacity = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                       label="Available Capacity")
    Price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="Ticket Price(CAD)")
    TotalPrice = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="Total Price")

    class Meta:
        model = packagebookingData
        fields = ['user', 'pid', 'People', 'AvailbleCapacity', 'Price', 'day', 'Comments', 'TotalPrice']
        labels = {'user': 'User', 'pid': 'Package', 'People': 'People',
                  'Price': 'Ticket Price(CAD)',
                  'day': 'Day of Booking', 'Comments': 'Comments', 'TotalPrice': 'Total Price'}
