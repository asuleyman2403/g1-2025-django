from django import forms
from .models import Product, Category


class CreateProductForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=200, required=True, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Enter product name'
    }))
    description = forms.CharField(min_length=0, max_length=2000, required=False, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Enter description'
    }))
    amount = forms.IntegerField(min_value=0, max_value=1000, required=True, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Enter product amount'
    }))
    price = forms.IntegerField(min_value=0, label='Price in KZT', required=True, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Enter price in KZT'
    }))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = ['name', 'price', 'description']
        fields = '__all__'
        widgets = {
            'name': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'amount': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Enter product amount'
            }),
            'description': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Enter description'
            }),
            'price': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Enter price in KZT'
            }),
            'category': forms.Select({
                'class': 'form-select',
            }),
        }


class CategoryProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'amount', 'price', 'description']
        widgets = {
            'name': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'amount': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Enter product amount'
            }),
            'description': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Enter description'
            }),
            'price': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Enter price in KZT'
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Enter category name'
            })
        }
