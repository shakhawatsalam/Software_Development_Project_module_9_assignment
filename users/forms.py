from django  import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from events.forms import StyleFormMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()
# REGISTRATION FORM USING  MODEL FORM
class RegistrationForm(StyleFormMixin, forms.ModelForm):
    password =  forms.CharField(widget=forms.PasswordInput)
    confirm_password =  forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','first_name', 'last_name', 'password','confirm_password']
        
    # PASSWORD FIELD ERROR HANDLING
    def clean_password(self):
        data = self.cleaned_data.get("password")
        
        return data
    
      
    # CHECKING EMAIL IS ALREADY EXISTS OR NOT  
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        
        if email_exists:
            raise forms.ValidationError("Email already exists")
        return email
    
    
    # CHECKING PASSAWORD AND CONFIRM PASSWORD FIELD IS SAME OR NOT
    def clean(self): # Non Field Error
        cleaned_data = super().clean()
        password =  cleaned_data.get('password')
        confirm_password =  cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match")
        return cleaned_data
    
    
    
# LOGIN FORM 
class LoginForm(StyleFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
# ASSIGN ROLE FORM
class AssignedRoleForm(StyleFormMixin,forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label="Select a Role"
    )
    
    class Meta:
        model = User
        fields = [] 
    
# CREATE GROUP FORM
class CreateGroupForm(StyleFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required= False,
        label='Assign Permission'
    )
    
    class Meta:
        model= Group
        fields= ['name',  'permissions']
        
        
# USER UPDATE FORM

class UpdateUserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name', 'last_name']
        
    


# Password Related Form  
class CustomPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass
class CustomPasswordResetConfirmForm(StyleFormMixin, SetPasswordForm):
    pass

class EditProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = CustomUser      
        fields = ['email', 'first_name', 'last_name', 'phone', 'profile_image']
    
    
    
    