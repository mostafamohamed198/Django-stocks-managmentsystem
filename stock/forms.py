
from django import forms
from .models import *

class CreateMealForm(forms.ModelForm):
    class Meta:
        model = watchlist
        fields = ['name']
    name = forms.CharField()
   
class DateInput(forms.DateInput):
    # input_type = 'datetime-local'
    input_type = 'date'

class CreateStock(forms.ModelForm):
    class Meta: 
        model = stock
        fields = ['name', 'symbol', 'boughtprice', 'expectedexitprice', 'stocktype', 'expectedtime', 'start', 'end']
        widgets = {
            'expectedtime': DateInput(),
            'start': DateInput(),
            'end': DateInput()
        }
   
#    name = models.CharField(max_length=200)
#     symbol = models.CharField(max_length=200)
#     boughtprice =models.IntegerField()
#     expectedexitprice = models.IntegerField()
#     stocktype = models.ForeignKey('types', on_delete=models.CASCADE,default=None)
#     timesubmitted = models.DateTimeField(auto_now_add=True)
#     expectedtime = models.DateTimeField()
#     start = models.DateField(default=None)
#     end = models.DateField(default=None)