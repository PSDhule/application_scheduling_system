from django.shortcuts import render, redirect
from .models import Doctor, User, Appointment, Service


# HOME PAGE
def home(request):
    return render(request, 'index.html')


# DOCTOR LIST
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors})


# REGISTER PAGE
def register(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        # Email check
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already registered!'
            })

        User.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        return redirect('/login/')

    return render(request, 'register.html')


# LOGIN PAGE
def login(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(
            email=email,
            password=password
        ).first()

        if user:
            request.session.flush()
            request.session['user_id'] = user.id
            request.session['name'] = user.name

            print("LOGIN SUCCESS USER ID:", user.id)
            return redirect('/dashboard/')

        return render(request, 'login.html', {'error': 'Invalid Email or Password'})

    return render(request, 'login.html')


# DASHBOARD
def dashboard(request):

    if 'user_id' not in request.session:
        return redirect('/login/')

    return render(request, 'dashboard.html', {
        'name': request.session['name']
    })


# LOGOUT
def logout(request):
    request.session.flush()
    return redirect('/')


# BOOK APPOINTMENT
def booking(request):

    if 'user_id' not in request.session:
        return redirect('/login/')

    doctors = Doctor.objects.all()
    services = Service.objects.all()

    context = {
        'doctors': doctors,
        'services': services
    }

    if request.method == "POST":

        patient_name = request.POST.get('patient_name')
        doctor_id = request.POST.get('doctor')
        service_id = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not patient_name or not doctor_id or not service_id or not date or not time:
            context['error'] = "All fields required"
            return render(request, 'booking.html', context)

        # SESSION USER
        user = User.objects.get(id=request.session['user_id'])

        # SELECTED DATA
        doctor = Doctor.objects.get(id=doctor_id)
        service = Service.objects.get(id=service_id)

        # CHECK SLOT
        already_booked = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time,
            status="Approved"
        ).exists()

        if already_booked:
            context['error'] = "Doctor not available. Appointment Rejected."
            return render(request, 'booking.html', context)

        # SAVE BOOKING
        Appointment.objects.create(
            user=user,
            patient_name=patient_name,
            doctor=doctor,
            service=service,
            date=date,
            time=time,
            status="Approved"
        )

        return redirect('/mybooking/')

    return render(request, 'booking.html', context)

# ADMIN BOOKINGS
def admin_booking(request):
    data = Appointment.objects.all()
    return render(request, 'admin_booking.html', {
        'data': data
    })


# APPROVE
def approve(request, id):
    obj = Appointment.objects.get(id=id)
    obj.status = "Approved"
    obj.save()

    return redirect('/admin-booking/')


# REJECT
def reject(request, id):
    obj = Appointment.objects.get(id=id)
    obj.status = "Rejected"
    obj.save()

    return redirect('/admin-booking/')

# MY BOOKINGS
def mybooking(request):

    if 'user_id' not in request.session:
        return redirect('/login/')

    user = User.objects.get(id=request.session['user_id'])
    data = Appointment.objects.filter(user=user)

    return render(request, 'mybooking.html', {'data': data})