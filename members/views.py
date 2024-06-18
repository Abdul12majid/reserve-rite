from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail, EmailMessage, send_mass_mail, EmailMultiAlternatives


# Create your views here.
def login_user(request):
	if request.method == 'POST':
		print('post method')
		email = request.POST['email']
		password = request.POST['password']
		user = User.objects.filter(email=email).exists()
		print(user)
		if user is True:
			get_user = User.objects.get(email=email)
			username = get_user.username

			#if not user.check_password():
			#	messages.success(request, ('wrong password'))
			#	return redirect(request.META.get("HTTP_REFERER"))
			
			user_ = authenticate(request, username=username, password=password)
			if user_ is not None:
				login(request, user_)
				print('Logged in')
				x = str(request.user.id)

				return redirect('home_index')
			else:
				print('incorrect password')
				messages.success(request, ('incorrect details'))
				return redirect('login-user')
		else:
			messages.success(request, ('Account does not exists, kindly create one.'))
			print('account does not exist')
			#return redirect('register')
	return render(request, 'login.html', {})


def register(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		username = first_name
		last_name = request.POST['last_name']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		if password1==password2:
			if User.objects.filter(username=username).exists():
				a = User.objects.filter(username=username).first()
				return render(request, 'register_user.html', {'first_name':first_name, 'username':username, 'last_name':last_name, 'email':email, 'a':a})
			elif User.objects.filter(email=email).exists():
				b = User.objects.filter(email=email).exists()
				return render(request, 'register_user.html', {'first_name':first_name, 'username':username, 'last_name':last_name, 'email':email, 'b':b})
			else:
				user = User.objects.create_user(first_name=first_name, username=username, last_name=last_name, email=email, password=password2)
				user.save()
				print(f'Registration successsful - {username}')
				get_user = User.objects.get(username=username)
				user=authenticate(username=username, password=password2)
				login(request, user)
				return redirect('home_index')
		else:
			messages.success(request, ('Password does not match, try again'))
			c = password1==password2
			return render(request, 'register_user.html', {'first_name':first_name, 'username':username, 'last_name':last_name, 'email':email, 'c':c})
	return render(request, 'register_user.html', {})