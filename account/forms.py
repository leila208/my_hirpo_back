from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField


User = get_user_model()

#-----------------------   Admin Forms  ---------------------------------------------------

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','company_name','surname','password1','password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserAdminChangeForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
        
    class Meta:
        model = User
        fields = ('email','name','surname', 'password1', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

