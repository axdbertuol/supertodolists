from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
# from accounts.models import CustomUUID
from .authentication import CustomAuthenticationBackend
from django.urls import reverse
from django.template.loader import get_template
# from .forms import SignupForm
from . import forms
# import accounts.forms


# def send_signup_email(request):
# 	email = request.POST['email']
# 	uuid = CustomUUID.objects.create(email=email)
# 	url = request.build_absolute_uri(
# 		reverse('login') + '?CustomUUID=' + str(uuid.uid))
# 	message_body = f'Use this link to log in:\n\n{url}'
# 	send_mail(
# 		'Your login link for Supertodolists',
# 		message_body,
# 		'noreply@supertodolists',
# 		[email],
# 	)
# 	messages.success(
# 		request,
# 		"Check your email, we've sent you a link you can use to log in."
# 	)
# 	return redirect('/')

def signup(request):
	# form = forms.SignupForm()
	if request.method == 'POST':
		form = forms.SignupForm(data=request.POST)
		if form.is_valid():
			print('oi')
			form.save()
			return redirect('/')
		else:
			render(request, 'accounts/signup.html', {'form': form})
	return render(request, 'accounts/signup.html', {'form': forms.SignupForm()})

def login_view(request):
	# form = forms.LoginForm()

	if request.method == 'POST':
		form = forms.LoginForm(request=request, data=request.POST)
		# print(form)
		if form.is_valid():
			user = auth.authenticate(
					request,
				 	email=form.cleaned_data.get('email'),
				 	password=form.cleaned_data.get('password')
					)
			auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

			return redirect('/')
		else:
			return render(request, 'accounts/login.html', {'form': form, 'error': form.errors})

	return render(request, 'accounts/login.html', {'form': forms.LoginForm()})

def logout_view(request):
	auth.logout(request)
	return redirect('/')
