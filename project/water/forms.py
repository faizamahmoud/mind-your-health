from django import forms
from .models import WaterIntake

#* water intake form to handle creating and updating water intake instances

class WaterIntakeForm(forms.ModelForm):
    class Meta:
        model = WaterIntake
        fields = ['intake', 'date']
        widgets = {
            'intake': forms.NumberInput(attrs={'step': '0.01'}),
        }

