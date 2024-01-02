from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import *
from .models import *

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Change 'home' to your actual home page URL
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your actual home page URL
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    # Your home view logic goes here
    return render(request, 'home.html')

def add_patient_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient added successfully.')
            return redirect('add_patient')  # Change 'home' to your actual home page URL
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donor_list.html', {'donors': donors})

def add_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor added successfully!')
            return redirect('donor_list')  # Redirect to your home page
    else:
        form = DonorForm()
    
    return render(request, 'add_donor.html', {'form': form})

def add_donation_record(request):
    if request.method == 'POST':
        form = DonationRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation record added successfully!')
            return redirect('blood_inventory')  # Replace 'home' with the actual URL name of your home page

    else:
        form = DonationRecordForm()

    return render(request, 'add_donation_record.html', {'form': form})

def hospital_list(request):
    hospitals = Hospital.objects.all()
    return render(request, 'hospital_list.html', {'hospitals': hospitals})

def hospital_detail(request, hospital_id):
    hospital = Hospital.objects.get(pk=hospital_id)
    return render(request, 'hospital_detail.html', {'hospital': hospital})

def hospital_create(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hospital_list')
    else:
        form = HospitalForm()

    return render(request, 'hospital_form.html', {'form': form, 'action': 'Create'})

def hospital_update(request, hospital_id):
    hospital = Hospital.objects.get(pk=hospital_id)

    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('hospital_list')
    else:
        form = HospitalForm(instance=hospital)

    return render(request, 'hospital_form.html', {'form': form, 'action': 'Update'})

def find_match(request, patient_id):
    # Get the patient based on the ID
    patient = Patient.objects.get(pk=patient_id)
    # Find donors with the same blood group as the patient
    matching_donors = Donor.objects.filter(blood_group=patient.blood_group)
    blood_availability = BloodInventory.objects.filter(blood_group=patient.blood_group).first()

    return render(request, 'find_match.html', {'patient': patient, 'matching_donors': matching_donors, 'blood_availability': blood_availability})

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    donation_records = DonationRecord.objects.filter(blood_type=patient.blood_group)
    return render(request, 'patient_detail.html', {'patient': patient, 'donation_records': donation_records})

def view_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    return render(request, 'patient_data.html', {'patient': patient})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')

    return render(request, 'delete_patient.html', {'patient': patient})

def update_blood_inventory():
    # Initialize blood inventory with zero quantities for each blood group
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    blood_inventory_data = {group: 0 for group in blood_groups}

    # Retrieve actual donation records and update quantities
    donation_records = DonationRecord.objects.all()
    for record in donation_records:
        blood_group = record.blood_type
        quantity = record.quantity
        # Update quantity in blood inventory
        blood_inventory_data[blood_group] += quantity

    # Update the BloodInventory model in the database
    for blood_group, quantity in blood_inventory_data.items():
        obj, created = BloodInventory.objects.update_or_create(
            blood_group=blood_group,
            defaults={'quantity': quantity}
        )

def blood_inventory(request):
    # Call the function to update the BloodInventory model
    update_blood_inventory()

    # Retrieve the blood inventory data from the database
    blood_inventory_data = BloodInventory.objects.all()

    return render(request, 'blood_inventory.html', {'blood_inventory': blood_inventory_data})

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            # Redirect to the patient list view after editing
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

def get_blood(request, patient_id):
    if request.method == 'POST':
        # Get the selected quantity from the form
        quantity = int(request.POST.get('quantity'))

        # Get the patient based on the ID
        patient = Patient.objects.get(pk=patient_id)

        # Find blood availability for the patient's blood group
        blood_availability = BloodInventory.objects.filter(blood_group=patient.blood_group).first()
        matching_donors = Donor.objects.filter(blood_group=patient.blood_group)

        # Check if there is enough blood available
        if blood_availability and blood_availability.quantity >= quantity:
            # Update blood availability in the database
            blood_availability.quantity -= quantity
            blood_availability.save()

            # Create a BloodTransaction instance
            transaction = BloodTransaction.objects.create(patient=patient, quantity_taken=quantity)

            # Save the transaction to the database
            transaction.save()

            # Redirect to a success page or any other page as needed
            messages.success(request, 'Blood taken successfully.')
            return redirect('find_match', patient_id=patient_id)
        else:
            # Redirect to a page indicating not enough blood available
            messages.error(request, 'Not enough blood available.')
            return redirect('find_match', patient_id=patient_id)
    # Handle other HTTP methods as needed
    return redirect('patient_list')

def view_transactions(request):
    transactions = BloodTransaction.objects.all()
    return render(request, 'view_transactions.html', {'transactions': transactions})
