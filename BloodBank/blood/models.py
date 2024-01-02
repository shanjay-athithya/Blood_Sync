# models.py
from django.db import models
from django.urls import reverse


class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Patient(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    doctor_name = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, default=None)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    #hospital_address = models.TextField()
    mobile_number = models.CharField(max_length=20)
    date_when_need = models.DateField()
    other_description = models.TextField()
    
    def get_edit_url(self):
        return reverse('edit_patient', args=[str(self.patient_id)])

    def __str__(self):
        return self.name

class Donor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    donor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    blood_group = models.CharField(max_length=5)
    contact_information = models.CharField(max_length=20)
    last_donation_date = models.DateField()
    
    def __str__(self):
        return self.name
       
class DonationRecord(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donation_date = models.DateField()
    quantity = models.IntegerField()
    blood_type = models.CharField(max_length=5)

    def save(self, *args, **kwargs):
        # Automatically set the blood type from the associated donor
        self.blood_type = self.donor.blood_group
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Donation ID: {self.pk}, Donor: {self.donor}, Donation Date: {self.donation_date.strftime('%Y-%m-%d')}, Blood Group: {self.blood_type}, Quantity: {self.quantity}"

class BloodInventory(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, primary_key=True, default='A+')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.blood_group} - Quantity: {self.quantity}"

class BloodTransaction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    quantity_taken = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient: {self.patient.name} - Quantity taken: {self.quantity_taken} units at {self.timestamp}"