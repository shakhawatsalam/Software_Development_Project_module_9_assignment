
from django import forms
from events.models  import  Event, Category,  Participant

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
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                        'class': self.default_classes,
                        'placeholder': f"Enter {field.label.lower()}"
                    })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                        'class': self.default_classes,
                        'placeholder': f"Enter {field.label.lower()}"
                    })
            else:
                # print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })






class EventModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 
            'description', 
            'date', 
            'time', 
            'location', 
            'category'
        ] 


class CategoryModelForm(StyleFormMixin,forms.ModelForm):
     class Meta:
        model = Category
        fields = [
            'name', 
            'description', 
        ] 
        
        

class ParticipantModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'name', 
            'email', 
            'events'
        ] 
        
        
        
        