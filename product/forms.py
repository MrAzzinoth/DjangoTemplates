from django import forms

from .models import Product, Comment


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-controls'}),
        }


