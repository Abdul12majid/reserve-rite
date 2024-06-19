from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking, Table, Status, Message, Notification
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	tables = Table.objects.filter(is_available=True)
	context = {
	"tables":tables,
	}
	return render(request, 'home_index.html', context)

def home_index(request):
	return render(request, 'home_index.html')

def book_home_table(request):
	get_status = Status.objects.get(id=1)
	if request.method == 'POST':
		if request.user.is_authenticated:
			user = request.user
			date = request.POST['date']
			time = request.POST['time']
			message = request.POST['message']
			table = request.POST['table']
			guests = request.POST['guests']
			table_id = Table.objects.get(id=table)
			name = user.username
			email = user.email
			contact = user.profile.contact
			#print(f'{user}\n{date}\n{time}\n{message}\n{table}')

			booking = Booking.objects.create(
				name=name, 
				email=email,
				contact=contact,
				date=date,
				time=time,
				message=message,
				table=table_id,
				status=get_status,
				guests=guests
				)

			booking.save()
			messages.success(request, ('Reservation made, details would be forwarded to your mail soon'))
			table_id.is_available = False
			table_id.save()
			book_id = Booking.objects.filter(name=name).last()
			get_book_id = book_id.id
			add_booking = user.profile.bookings.add(get_book_id)
			user.profile.save()
			return redirect('reserve_index')
			print(f'{date}, {message}, {time}')


		else:
			name = request.POST['name']
			email = request.POST['email']
			contact = request.POST['contact']
			date = request.POST['date']
			time = request.POST['time']
			message = request.POST['message']
			table = request.POST['table']
			table_id = Table.objects.get(id=table)
			guests = request.POST['guests']
			booking = Booking.objects.create(
				name=name, 
				email=email,
				contact=contact,
				date=date,
				time=time,
				message=message,
				table=table_id,
				status=get_status,
				guests=guests,
				)
			booking.save()
			messages.success(request, ('reservations successfully made'))
			print(f'{date}, {message}, {time}')

	return redirect('index')

@login_required(login_url='login-user')
def reservations(request):
	bookings = request.user.profile.bookings.all().order_by('-id')
	context = {
	"bookings":bookings,
	
	}
	return render(request, 'reservations.html', context)


def cancel_reservation(request, pk):
	cancel = Status.objects.get(id=3)
	pending = Status.objects.get(id=2)
	approved = Status.objects.get(id=1)
	get_booking = Booking.objects.get(id=pk)
	if get_booking.status.name == "Approved":
		print('approved')
		messages.success(request, "Reservation already approved, can't cancel.")
	elif get_booking.status.name == "Pending":
		get_booking.status = cancel
		
		get_booking.save()
		
		get_booking.table.is_available = True
		get_booking.table.save()
		
		messages.success(request, "Reservation cancelled.")
	elif get_booking.status.name == "Cancelled":
		print('cancel')
		messages.success(request, "Reservation already cancelled.")
	
	return redirect(request.META.get("HTTP_REFERER"))


def book_table(request):
	tables = Table.objects.filter(is_available=True)
	context = {
	"tables":tables,
	}
	return render(request, 'book_table.html', context)

def about(request):
	tables = Table.objects.filter(is_available=True)
	context = {
	"tables":tables,
	}
	return render(request, 'about.html', context)

def contact(request):
	if request.method == "POST":
		if request.user.is_authenticated:
			user = request.user
			message = request.POST['message']
			name = user.username
			email = user.email
			save_message = Message.objects.create(
				name=name, 
				email=email, 
				message=message
				)
			save_message.save()
		
			context = {
				'user':user
			}
			messages.success(request, (f'Hi {user.username}, Your message has been received, kindly await reply.'))
			return render(request, 'contact.html', context)
		else:
			message = request.POST['message']
			name = request.POST['name']
			email = request.POST['email']
			save_message = Message.objects.create(
				name=name, 
				email=email, 
				message=message
				)
			save_message.save()
			messages.success(request, (f'Hi {name}, Your message has been received, kindly await reply.'))
		return render(request, 'contact.html')
	
	return render(request, 'contact.html')


@login_required(login_url='login-user')
def reserve_index(request):
	user = request.user
	bookings = user.profile.bookings.all().order_by('-id')[:3]
	#print(bookings)
	tables = Table.objects.filter(is_available=True)
	notifications = Notification.objects.all().order_by('-id')
	notification_count = Notification.objects.count()
	context = {
	"tables":tables,
	'user':user,
	'bookings':bookings,
	'notifications':notifications,
	'notification_count':notification_count,
	}
	return render(request, 'reserve_index.html', context)

def profile(request):
	user = request.user
	if request.method == "POST":
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		contact = request.POST['contact']
		user.first_name = first_name
		user.username = first_name
		user.last_name = last_name
		user.email = email
		user.profile.contact = contact
		user.save()
		user.profile.save()
		messages.success(request, ('Info successfully updated.'))
		return redirect('reserve_index')

	return render(request, 'profile.html')


def details(request, pk):
	get_booking = Booking.objects.get(id=pk)
	get_booking = Booking.objects.get(id=26)
	print(get_booking.status.name)

	context = {
		'get_booking':get_booking
	}
	return render(request, 'details.html', context)

def edit_reservation(request, pk):
	user = request.user
	get_booking = Booking.objects.get(id=pk)
	tables = Table.objects.filter(is_available=True)
	if request.method == 'POST':
		date = request.POST['date']
		time = request.POST['time']
		message = request.POST['message']
		table = request.POST['table']
		table_id = Table.objects.get(id=table)

		guests = request.POST['guests']
		table_id = Table.objects.get(id=table)
		get_booking.date = date
		get_booking.time = time
		get_booking.message = message
		get_booking.table = table_id
		get_booking.save()
		messages.success(request, ('Reservation successfully updated.'))

	
	context = {
		'get_booking':get_booking,
		'tables':tables
	}
	return render(request, 'update_reservation.html', context)

