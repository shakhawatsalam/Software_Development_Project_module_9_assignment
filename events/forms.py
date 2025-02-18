
from django import forms
from events.models  import  Event, Category

class StyleFormMixin:
    default_classes ="w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out"
    
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_style_widgets()
        
        
    def  apply_style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                        'class': self.default_classes,
                        'placeholder': f"Enter {field.label.lower()}"
                    })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                        'class': "p-2 mx-5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555]",
                        'placeholder': f"Enter {field.label.lower()}"
                    })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                 field.widget.attrs.update({
                        'class': 'w-0 max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
                        'placeholder': f"Enter {field.label.lower()}"
                    })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })






class EventModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 
            'description', 
            'image',
            'date', 
            'time', 
            'location', 
            'category'
        ] 
        widgets ={
            'date':  forms.SelectDateWidget,
            'time': forms.TimeInput(attrs={
                'type': 'time',  # Enables HTML5 time picker in supporting browsers
                'class': "p-2 mx-5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555]",
                'placeholder': "Enter time"
            }),
        }


class CategoryModelForm(StyleFormMixin,forms.ModelForm):
     class Meta:
        model = Category
        fields = [
            'name', 
            'description', 
        ] 
        
        


        
        
        
        