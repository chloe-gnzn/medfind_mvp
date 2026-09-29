from django import forms

from home_app.models import Medicine, MedicineCategory


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-input')


class CategoryForm(StyledModelForm):
    class Meta:
        model = MedicineCategory
        fields = ['category_name', 'description']
        widgets = {
            # category_name is a text column in the ERD; a one-line input is friendlier
            'category_name': forms.TextInput(attrs={'placeholder': 'e.g. Pain relievers'}),
            'description': forms.TextInput(attrs={'placeholder': 'Short description'}),
        }


class MedicineForm(StyledModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'generic_name', 'category', 'form', 'strength', 'description']
        widgets = {
            'medicine_name': forms.TextInput(attrs={'placeholder': 'Brand name, e.g. Biogesic'}),
            'generic_name': forms.TextInput(attrs={'placeholder': 'e.g. Paracetamol'}),
            'form': forms.TextInput(attrs={'placeholder': 'tablet, capsule, syrup...'}),
            'strength': forms.TextInput(attrs={'placeholder': 'e.g. 500 mg'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
