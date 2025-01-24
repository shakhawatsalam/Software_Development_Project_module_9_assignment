
from django import forms
from events.models  import  Event, Category,  Participant

class StyleFromMixin:
    default_classes ="w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out"
    def  apply_style_widgets(self):
        pass

class EventModelForm(forms.ModelForm):
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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
                'placeholder': 'Enter event name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
                'placeholder': 'Enter event description',
                'rows': 4,
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
                'placeholder': 'Enter event locationsss',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
            }),
        }


class CategoryModelForm(forms.ModelForm):
     class Meta:
        model = Category
        fields = [
            'name', 
            'description', 
        ] 
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
                'placeholder': 'Enter category Name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
                'placeholder': 'Enter event description',
                'rows': 4,
            }),
        }
        

class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'name', 
            'email', 
            'events'
        ] 
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
                'placeholder': 'Enter participant name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full max-w-lg p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#213555] mb-5 transition duration-300 ease-in-out',
                'placeholder': 'Enter participant email',
            }),
            'events': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2',
            }),
        }
        
        
        