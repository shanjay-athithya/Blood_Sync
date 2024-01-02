from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', custom_login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('add_patient/', add_patient_view, name='add_patient'),
    path('donor_list/', donor_list, name='donor_list'),
    path('add_donor/', add_donor, name='add_donor'),
    path('add_donation_record/', add_donation_record, name='add_donation_record'),
    path('hospitals/', hospital_list, name='hospital_list'),
    path('hospitals/<int:hospital_id>/', hospital_detail, name='hospital_detail'),
    path('hospitals/create/', hospital_create, name='hospital_create'),
    path('hospitals/<int:hospital_id>/update/', hospital_update, name='hospital_update'),
    path('find_match/<int:patient_id>/', find_match, name='find_match'),
    path('patients/', patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', view_patient, name='view_patient'),
    path('patient_detail/<int:patient_id>/', patient_detail, name='patient_detail'),
    path('find_match/<int:patient_id>/', find_match, name='find_match'),
    path('blood_inventory/', blood_inventory, name='blood_inventory'),
    path('delete_patient/<int:patient_id>/', delete_patient, name='delete_patient'),
    path('edit_patient/<int:patient_id>/', edit_patient, name='edit_patient'),
    path('get_blood/<int:patient_id>/', get_blood, name='get_blood'),
    path('view_transactions/', view_transactions, name='view_transactions'),
    # Add other URLs as needed
]
