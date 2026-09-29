from django import forms

from home_app.models import Medicine

from .models import Inventory

ALLOWED_EXTENSIONS = ('.pdf', '.jpg', '.jpeg', '.png')
MAX_UPLOAD_MB = 5


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['medicine', 'price', 'availability_status', 'stock_quantity']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'stock_quantity': forms.NumberInput(attrs={'min': '0'}),
        }

    def __init__(self, *args, pharmacy=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-input')
        if self.instance.pk:
            # editing: the medicine can't be swapped, only its price/stock
            self.fields['medicine'].disabled = True
        elif pharmacy is not None:
            # adding: hide medicines this pharmacy already lists
            self.fields['medicine'].queryset = (
                Medicine.objects.exclude(inventory_items__pharmacy=pharmacy)
                .select_related('category')
            )


class VerificationUploadForm(forms.Form):
    document = forms.FileField(
        label='Business permit / license (PDF, JPG or PNG, max 5 MB)',
        widget=forms.ClearableFileInput(attrs={'class': 'form-input'}),
    )

    def clean_document(self):
        doc = self.cleaned_data['document']
        if not doc.name.lower().endswith(ALLOWED_EXTENSIONS):
            raise forms.ValidationError('Please upload a PDF, JPG or PNG file.')
        if doc.size > MAX_UPLOAD_MB * 1024 * 1024:
            raise forms.ValidationError(f'File is too large (max {MAX_UPLOAD_MB} MB).')
        return doc
