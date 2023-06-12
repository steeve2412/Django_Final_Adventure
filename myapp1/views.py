from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from myapp1.models import *
from django.contrib import messages
from myapp1.forms import BookingForm, PacakgesForm, BookPacakgesForm
from myapp1.models import bookingData, ContactUSData
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .helpers import send_forget_password_mail
import uuid
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and user.is_superuser


# Create your views here.
def Test(request):
    return render(request, 'myapp1/generic.html')


def index1(request):
    return render(request, 'myapp1/index1.html')


def index(request):
    return render(request, "myapp1/index1.html", {})


def BookedRecords(request):
    orders = bookingData.objects.all()
    msg = 'Order Placed!'
    return render(request, 'myapp1/bookingRecords.html', {'orders': orders})


def NotAuthorized(request):
    return render(request, 'myapp1/NotAuthorized.html')


def mybookings(request):
    orders = bookingData.objects.filter(user=1)
    msg = 'Order Placed!'
    return render(request, 'myapp1/mybookings.html', {'orders': orders})


def BookedPackageRecords(request):
    orders = packages.objects.all()
    msg = 'Order Placed!'
    return render(request, 'myapp1/mypackages.html', {'orders': orders})


@user_passes_test(is_admin)
def ContactUSRecords(request):
    if request.user.is_authenticated:
        orders = ContactUSData.objects.all()
        msg = 'Order Placed!'
        return render(request, 'myapp1/contactusdetails.html', {'orders': orders})
    else:
        return render(request, 'myapp1/login.html')


def userpackages(request):
    orders = packagebookingData.objects.filter()
    msg = 'Order Placed!'
    return render(request, 'myapp1/userbookingpacakage.html', {'orders': orders})


# Create your views here.
def BookingAdventure(request):
    msg = ''
    if request.method == 'POST':
        order_form = BookingForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            deduct_capacity(order.aid, order.People, order.day)
            order.refresh_from_db()
            orders = bookingData.objects.all()
            msg = 'Order Placed!'
            return render(request, 'myapp1/bookingRecords.html', {'orders': orders})
    else:
        order_form = BookingForm()
        adventuredata = adventure.objects.all()
    return render(request, 'myapp1/bookingtemplate.html', {'order_form': order_form})


def updateBookingAdventure(request, id):
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(bookingData, booking_Id=id)

    # pass the object as instance in form
    form = BookingForm(request.POST or None, instance=obj)
    if form.is_valid():
        order = form.save(commit=False)
        order.save()
        if obj.People < order.People:
            return_capacity(order.aid, order.People, order.day)
        else:
            deduct_capacity(order.aid, order.People, order.day)

        orders = bookingData.objects.all()
        msg = 'Order Placed!'
        return render(request, 'myapp1/bookingRecords.html', {'orders': orders})

    # add form dictionary to context
    context["form"] = form

    return render(request, "myapp1/editbookingtemplate.html", context)


def deleteBookingAdventure(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(bookingData, booking_Id=id)

    if request.method == "POST":
        # delete object
        return_capacity(obj.aid, obj.People, obj.day)
        obj.delete()
        # after deleting redirect to
        # home page
        orders = bookingData.objects.all()
        msg = 'Order Placed!'
        return render(request, 'myapp1/bookingRecords.html', {'orders': orders})

    return render(request, "myapp1/deletebookingtemplate.html", context)


def get_capacity(request):
    # Get the continent ID from the AJAX request
    aid = request.GET.get('id')
    day = request.GET.get('adate')

    # capacitydata = schedule.objects.filter(adv_id=aid)
    capacitydata = schedule.objects.get(Q(adv_id=aid) & Q(schedule_date=day))
    pricedata = adventure.objects.filter(id=aid)

    data1 = [{'capacity': capacitydata.capacity}]
    data2 = [{'price': prices.price} for prices in pricedata]

    data = {'data1': data1, 'data2': data2}

    # Return the data as a JSON response
    # data = [{'capacity': capacity.capacity} for capacity in capacitydata]
    return JsonResponse(data, safe=False)


def deduct_capacity(aid, people, day):
    # Get the product and warehouse objects
    # capacitydata = schedule.objects.get(adv_id=aid )
    capacitydata = schedule.objects.get(Q(adv_id=aid) & Q(schedule_date=day))

    # Deduct the stock from the product and warehouse
    capacitydata.capacity -= people

    # Save the changes
    capacitydata.save()


def get_pacakagecapacity(request):
    # Get the continent ID from the AJAX request
    pid = request.GET.get('id')
    day = request.GET.get('adate')

    # capacitydata = schedule.objects.filter(adv_id=aid)
    capacitydata = packages.objects.get(Q(id=pid) & Q(day=day))

    data1 = [{'capacity': capacitydata.capacity}]
    data2 = [{'price': capacitydata.price}]

    data = {'data1': data1, 'data2': data2}

    # Return the data as a JSON response
    # data = [{'capacity': capacity.capacity} for capacity in capacitydata]
    return JsonResponse(data, safe=False)


def deduct_pacakgecapacity(pid, people, day):
    # Get the product and warehouse objects
    # capacitydata = schedule.objects.get(adv_id=aid )

    capacitydata = packages.objects.get(Q(package_name=pid) & Q(day=day))

    # Deduct the stock from the product and warehouse
    capacitydata.capacity -= people

    # Save the changes
    capacitydata.save()


def return_pacakgecapacity(pid, people, day):
    # Get the product and warehouse objects
    # capacitydata = schedule.objects.get(adv_id=aid )

    capacitydata = packages.objects.get(Q(package_name=pid) & Q(day=day))

    # Deduct the stock from the product and warehouse
    capacitydata.capacity += people

    # Save the changes
    capacitydata.save()


def return_capacity(aid, people, day):
    # Get the product and warehouse objects
    #  capacitydata = schedule.objects.get(adv_id=aid)
    capacitydata = schedule.objects.get(Q(adv_id=aid) & Q(schedule_date=day))

    # Deduct the stock from the product and warehouse
    capacitydata.capacity += people

    # Save the changes
    capacitydata.save()


from django.core.mail import EmailMessage
from django.shortcuts import render


def EmailData(client, people, email):
    # name = request.POST.get('name')
    # email = request.POST.get('email')
    # message = request.POST.get('message')

    # Create the email message
    subject = f'New message from {client}'
    body = f'{people} ({client}) sent a message:\n\n{"Hello There"}'
    sender = 'dhruvi1411patel@gmail.com'
    recipients = [{email}]
    # email_message = EmailMessage(subject, body, sender, recipients)
    send_mail(subject, body, sender, recipients)

    # Send the email
    # email_message.send()


# / return JsonResponse("true", safe=False)

# Create your views here.
@user_passes_test(is_admin)
def PackageAdventures(request):
    msg = ''
    if request.method == 'POST':
        order_form = PacakgesForm(request.POST)
        order = order_form.save(commit=False)
        order.save()
        orders = packages.objects.all()
        msg = 'Order Placed!'
        return render(request, 'myapp1/mypackages.html', {'orders': orders})
    else:
        order_form = PacakgesForm()

    return render(request, 'myapp1/packageTemplate.html', {'order_form': order_form})

def user_login(request):
    if request.method == 'GET':
        if 'username' in request.COOKIES:
            context = {
                'username': request.COOKIES['username'],
            }
            return render(request, 'myapp1/index1.html', context)
        else:
            return render(request, 'myapp1/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp1:index1'))
                response.set_cookie('username', username)
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp1/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp1:index1'))
    response.delete_cookie('username')


def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change_password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change_password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('')

    except Exception as e:
        print(e)
    return render(request, 'myapp1/change_password.html', context)


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget_password/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            print(f"\n{token}\n")
            profile_obj, created = Profile.objects.get_or_create(user=user_obj,
                                                                 defaults={'forget_password_token': f'{token}'})
            profile_obj.save()
            current_url = request.scheme + '://' + request.get_host()  # for getting dynamic url(included PORT number) for current project
            send_forget_password_mail(user_obj.email, token, current_url)  # inside  Helper.py file
            messages.success(request, f'An email is sent to {user_obj.email}.')
            return render(request, 'myapp1/forget_password_done.html')
    except Exception as e:
        print(e)
    return render(request, 'myapp1/forget_password.html')


def PackageAdventures(request):
    msg = '';
    if request.method == 'POST':
        order_form = PacakgesForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            order_form.save_m2m()
            orders = packages.objects.all()
            msg = 'Order Placed!'
            return render(request, 'myapp1/mypackages.html', {'orders': orders})
    else:
        order_form = PacakgesForm()

    return render(request, 'myapp1/packageTemplate.html', {'order_form': order_form})


def updatePacakageAdventure(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(packages, id=id)

    # pass the object as instance in form
    form = PacakgesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        order = form.save(commit=False)
        order.save()
        form.save_m2m()
        orders = packages.objects.all()
        msg = 'Order Placed!'
        return render(request, 'myapp1/mypackages.html', {'orders': orders})

    # add form dictionary to context
    context["form"] = form

    return render(request, "myapp1/editbookingtemplate.html", context)


def deletePacakageAdventure(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(packages, id=id)

    if request.method == "POST":
        # delete object
        # return_capacity(obj.aid, obj.People,obj.day)
        obj.delete()
        # after deleting redirect to
        # home page
        orders = packages.objects.all()
        msg = 'Order Placed!'
        return render(request, 'myapp1/mypackages.html', {'orders': orders})

    return render(request, "myapp1/deletePackagetemplate.html", context)


def PacakageBookingAdventure(request):
    msg = '';
    if request.method == 'POST':
        order_form = BookPacakgesForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            deduct_pacakgecapacity(order.pid, order.People, order.day)
            orders = packagebookingData.objects.all()
            msg = 'Order Placed!'
            return render(request, 'myapp1/userbookingpacakage.html', {'orders': orders})
    else:
        order_form = BookPacakgesForm()
    return render(request, 'myapp1/bookingpacakagetemplate.html', {'order_form': order_form})


def updateUserPacakageAdventure(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(packagebookingData, package_Id=id)

    # pass the object as instance in form
    form = BookPacakgesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        order = form.save(commit=False)
        order.save()

        if (obj.People < order.People):
            return_pacakgecapacity(order.pid, order.People, order.day)
        else:
            deduct_pacakgecapacity(order.pid, order.People, order.day)

        orders = packagebookingData.objects.all()
        msg = 'Order Placed!'
        return render(request, 'myapp1/userbookingpacakage.html', {'orders': orders})

    # add form dictionary to context
    context["form"] = form

    return render(request, "myapp1/edituserpacakgeTemplate.html", context)


def deleteUserPacakageAdventure(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(packagebookingData, package_Id=id)

    if request.method == "POST":
        # delete object
        return_pacakgecapacity(obj.pid, obj.People, obj.day)
        obj.delete()
        # after deleting redirect to
        # home page
        orders = packagebookingData.objects.all()
        msg = 'Order Placed!'
        return render(request, 'myapp1/userbookingpacakage.html', {'orders': orders})

    return render(request, "myapp1/deleteuserpackagebookingtemplate.html", context)


def save_data(request):
    # Get the submitted data
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')

    # Create a new instance of MyModel and save it to the database
    mymodel = ContactUSData(name=name, email=email, message=message)
    mymodel.save()

    # Return a success response
    # return HttpResponse('Data saved successfully!')
    return render(request, 'myapp1/contactussaved.html')
