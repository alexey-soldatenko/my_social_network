from django import forms 
from auth_user.models import MyUser

class LoginForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Электронная почта*'}), required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль*'}), required=True)

class RegForm(forms.Form):
	user_name = forms.CharField(max_length=100,
		widget=forms.TextInput(attrs={'placeholder': 'Имя и фамилия*'}), required=True)
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Электронная почта*'}), required=True)
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль*'}), required=True)
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль*'}), required=True)

class ImageForm(forms.ModelForm):
	class Meta:
		model = MyUser
		fields = ('person_id', 'avatar')

class SettingForm(forms.Form):
	person_id = forms.CharField(max_length=10)
	username = forms.CharField(max_length=100)
	city = forms.CharField(max_length=100)
	country = forms.CharField(max_length=100)
	email = forms.EmailField()

	