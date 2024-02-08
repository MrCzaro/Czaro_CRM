from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth.decorators import login_required



from django.utils import timezone
from .models import Department, Hospitalization, Observation
from .forms import DepartmentForm, ObservationForm, HospitalizationForm, TransferPatientForm, DischargeFrom
from patient.models import Patient

@login_required(login_url="/login/")
def hospitalization_detail(request, hospitalization_id):
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id)
    observations = Observation.objects.filter(hospitalization=hospitalization)
    context = {
        "title" : "Hospitalization Detail",
        "hospitalization" : hospitalization,
        "observations" : observations
    }
    
    return render(request, "hospitalization_detail.html", context)


@login_required(login_url="/login/")
def admit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = HospitalizationForm(request.POST)
        if form.is_valid():
            hospitalization = form.save(commit=False)
            department_id = request.POST.get('department_id')  # Assuming you have a hidden field in your form with the department_id
            department = get_object_or_404(Department, id=department_id)
            hospitalization.patient = patient
            hospitalization.department = department  # Associate the patient with the selected department
            hospitalization.save()
            return redirect('department:department_detail', department_id)
    else:
        form = HospitalizationForm()

    departments = Department.objects.all()  # Fetch all departments to display in the form

    context = {
        'form': form,
        'departments': departments,
        'title': f'Admit {patient.first_name} {patient.last_name}',
        'patient': patient,
    }

    return render(request, 'admit_patient.html', context)

@login_required(login_url="/login/")
def transfer_patient(request, patient_id, hospitalization_id):
    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id, patient=patient)
    
    if request.method == "POST":
        form = TransferPatientForm(request.POST)
        if form.is_valid():
            new_department = form.cleaned_data['department']
            hospitalization.department = new_department
            hospitalization.save()
            return redirect("department:department_detail", new_department.id)
    else:
        form = TransferPatientForm()
    
    context = {
        "form" : form,
        "title" : "Transfer Patient",
        "patient" : patient,
        "hospitalization" : hospitalization,
        "departments" : Department.objects.all()
    }
    
    return render(request, "transfer_patient.html", context)

@login_required(login_url="/login/")
def discharge_patient(request, hospitalization_id):
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id)
    
    if request.method == "POST":
        form = DischargeFrom(request.POST)
        if form.is_valid():
            dicharge_date = form.cleaned_data['dicharge_date']
            hospitalization.dicharged_on = dicharge_date
            hospitalization.is_discharged = True
            hospitalization.save()
            return redirect("department:department_detail", hospitalization.department.id)
    else:
        form = DischargeFrom()
        
    context = {
        "form" : form,
        "title" : "Discharge Patient",
        "hospitalization" : hospitalization
    }
    
    return render(request, "discharge_patient.html", context)
        
@login_required(login_url="/login/")
def department_detail(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    hospitalizations = Hospitalization.objects.filter(department__id=department_id, is_discharged=False)
    
    context = {
        "title" : "Department Detail",
        'hospitalizations': hospitalizations,
        "department" : department,
    }
    
    return render(request, "department_detail.html", context)

@login_required(login_url="/login/")
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            # Add the created_by field based on the logged-in user
            form.instance.created_by = request.user
            form.save()
            return redirect('department:department_list')  # Adjust the redirect URL
    else:
        form = DepartmentForm()

    context = {
        'form': form,
        'title': 'Create Department',
    }

    return render(request, 'create_department.html', context)


@login_required(login_url="/login/")
def department_list(request):
    departments = Department.objects.all()
    context = {
        'title': 'Department List',
        'departments': departments,
    }
    return render(request, 'department_list.html', context)




@login_required(login_url = "/login/")
def add_patient_observation(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")
    
    
    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization= get_object_or_404(Hospitalization, id=hospitalization_id, patient=patient)
    
    if request.method == "POST":
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.created_by = request.user
            observation.hospitalization = hospitalization
            observation.save()
            return redirect("department:hospitalization", hospitalization.id)
    else:
        
        form = ObservationForm()
        
    context = {
        "form" : form, 
        "title" : "Add Patient Observation",
        "patient_id" : patient.id,
    }
    
    return render(request,"patient_observation_form.html", context)

@login_required(login_url = "/login/")
def edit_patient_observation(request, patient_id, hospitalization_id, observation_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")
    
    patient = get_object_or_404(Patient, id = patient_id)
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id, patient=patient)
    observation = get_object_or_404(Observation, id=observation_id, hospitalization=hospitalization)
    
    if request.method == "POST":
        form = ObservationForm(request.POST, instance=observation)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization.id)
    else:
        form = ObservationForm(instance=observation)
        
    context = {
        "form": form,
        "title" : "Edit Patient Observation",
        "patient_id" : patient.id,
    }
    
    return render(request, "patient_observation_form.html", context)