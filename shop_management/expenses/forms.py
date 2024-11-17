from django import forms
from .models import Expense, Category
from datetime import datetime

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'description']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'value': datetime.now().strftime('%Y-%m-%d')
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['category'].choices = [
            (category.id, category.name) for category in categories
        ]
        self.fields['category'].widget.choices = [
            (category.id, category.name) for category in categories
        ]
        for category in categories:
            self.fields['category'].widget.attrs.update({
                f'data-description-{category.id}': category.description
            })
