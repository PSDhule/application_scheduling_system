from django.db import models


# USER
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# SPECIALIZATION
class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# DOCTOR
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    experience = models.IntegerField()
    fee = models.IntegerField()

    def __str__(self):
        return self.name


# SERVICE
class Service(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    duration = models.IntegerField()

    def __str__(self):
        return self.service_name


# TIMESLOT
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


# APPOINTMENT
class Appointment(models.Model):
    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100) 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()   

    status = models.CharField(max_length=20, choices=STATUS, default="Pending")

    def __str__(self):
        return f"{self.user.name} - {self.date} - {self.time}"

# PAYMENT
class Payment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)

    def __str__(self):
        return self.payment_status