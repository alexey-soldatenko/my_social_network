from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from auth_user.models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_bytes, force_text
from tokens import account_activation_token
from auth_user.forms import RegForm, LoginForm
from django.conf import settings
import os

def new_person_id():
	''' функция для определения номера person_id нового пользователя, взависимости от номера предыдущего.'''
	try: 
		last_person = MyUser.objects.latest('person_id')
	except:
		return 1000
	else:
		return last_person.person_id + 1


# Create your views here.
def signup_page(request):
	''' функция для отображения страницы регистрации'''
	if request.method == 'GET':
		form = RegForm()
		return render(request, 'signup.html', {'form':form})


def user_login(request):
	''' функция для обработки запроса на авторизацию'''
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password"]
			try:
				user = MyUser.objects.get(email=email)
			except MyUser.DoesNotExist:
				return HttpResponse("Вас не существует")
			if not user.is_active:
				return HttpResponse("Вы не активировали свой аккаунт")
			user_auth = authenticate(email=user.email, password=password)
			login(request, user_auth)
			user_page = '/person/id_{0}'.format(user.person_id)
			return redirect(user_page)
		else:
			return HttpResponse("bad validation")

def signup_save(request):
	''' функция для регистрации нового пользователя в системе'''
	if request.method == 'POST':
		form = RegForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data["user_name"]
			email = form.cleaned_data["email"]
			password1 = form.cleaned_data["password1"]
			password2 = form.cleaned_data["password2"]
			if password1 == password2:
				#создаем пользователя в бд, делаем его неактивным
				person_id = new_person_id()
				try:
					user = MyUser.objects.create_user(username=user_name, email=email, password=password1, person_id=person_id)
					user.is_active = False
					path_to_avatar = os.path.join(settings.MEDIA_URL, 'logo-img.png') 
					user.avatar = path_to_avatar
					user.save()
				except Exception as err:
					print(err)
					return HttpResponse("Пользователь уже зарегистрирован по данной почте.")
				#создаем письмо с активационной ссылкой
				current_site = get_current_site(request)
				mail_subject = 'Активируйте ваш аккаунт на сайте {0}'.format(current_site)
				message = render_to_string(
					'activate_message.html',
					{
					'user':user,
					'domain':current_site,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user)
					}
					)
				to_email = email
				send_mail(
					mail_subject,
					message,
					'your@gmail.com',
					[to_email],
					html_message=message
					)
			return HttpResponse("На указанный вами адрес электронной почты было отправлено письмо с сылкой для активации вашего аккаунта. Проверьте ваш почтовый ящик и подвердите его активность, перейдя по ссылке.")
		else:
			return render(request, 'signup.html', {'form':form})

def activate_account(request, uidb64, token):
	''' функция для активации аккаунта, при переходе по активационной ссылке'''
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = MyUser.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
		user = None
	if user and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)
		user_page = '/person/id_{0}'.format(user.person_id)
		return redirect(user_page)
	else:
		return HttpResponse("Nooo!")

def user_logout(request):
	''' функция выхода пользователя из системы'''
	logout(request)
	return redirect(request.META.get('HTTP_REFERER'))