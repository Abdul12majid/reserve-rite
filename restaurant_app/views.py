from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking, Table, Status, Message
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
				)

			booking.save()
			messages.success(request, ('reservations successfully made'))
			table_id.is_available = False
			table_id.save()
			book_id = Booking.objects.filter(name=name).last()
			get_book_id = book_id.id
			add_booking = user.profile.bookings.add(get_book_id)
			user.profile.save()
			print(f'{date}, {message}, {time}')


		else:
			name = request.POST['name']
			email = request.POST['email']
			contact = request.POST['contact']
			date = request.POST['date']
			time = request.POST['time']
			message = request.POST['message']
			table = request.POST['table']
			booking = Booking.objects.create(
				name=name, 
				email=email,
				contact=contact,
				date=date,
				time=time,
				message=message,
				table=table,
				status=get_status,
				)
			booking.save()
			messages.success(request, ('reservations successfully made'))
			print(f'{date}, {message}, {time}')

	return redirect('index')

@login_required(login_url='login-user')
def reservations(request):
	reservations_made = request.user.profile.bookings.all().order_by('-id')
	context = {
	"reservations_made":reservations_made,
	"full_reservations": [booking for booking in reservations_made],  # Include full details
	}
	return render(request, 'reservations.html', context)

@login_required(login_url='login-user')
def details(request, pk):
	user_id = request.user.id
	reserve = Booking.objects.get(id=pk)
	context = {
		"reserve":reserve,
	}
	return render(request, 'details.html', context)

def cancel_reservation(request, pk):
	get_booking = Booking.objects.get(id=pk)
	get_booking.table.is_available = True
	get_booking.table.save()
	get_booking.delete()
	return redirect('reservations')


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