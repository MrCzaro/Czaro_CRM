from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth.decorators import login_required



from django.utils import timezone
from .models import Department, Hospitalization, Observation
from .forms import DepartmentForm, ObservationForm
from patient.models import Patient




@login_required(login_url="/login/")
def department_detail(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    context = {
        "title" : "Department Detail",
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


@login_required(login_url="/login/")
def admitted_patients(request, department_id):
    # Assuming you have a Department model with an appropriate relationship to Visit
    department = get_object_or_404(Department, id=department_id)

    # Filter currently admitted patients in the specified department
    admitted_patients = Hospitalization.objects.filter(
        is_discharged=False,
        department=department 
    )

    context = {
        "department": department,
        "admitted_patients": admitted_patients,
        "title": "Admitted Patients",
    }

    return render(request, "admitted_patients.html", context)

@login_required(login_url="/login/")
def admit_patient(request, patient_id, hospitalization_id, department_id):
    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id, patient=patient)
    department = get_object_or_404(Department, id=department_id)
    
    # Check if the patient is already admitted in another department for the same visit:
    if Hospitalization.objects.filter(patient=patient, hospitalization=hospitalization).exists():
        context = {
            "title" : "Admission Error",
            "patient" : patient,
            "hospitalization" : hospitalization,
        }
        
        return render(request, "admit_error.html", context)
    # Admission logic
    hospitalization = Hospitalization(patient=patient, hospitalization=hospitalization, department=department)
    hospitalization.save()
    
    return redirect("department:detail", department_id=department.id)

    

@login_required(login_url="/login/")
def discharge_patient(request, patient_id, hospitalization_id, department_id):
    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id, patient=patient)
    department = get_object_or_404(Department, id=department_id)

    # Discharge logic
    hospitalization = Hospitalization.objects.get(patient=patient, hospitalization=hospitalization, department=department)
    hospitalization.discharged_on = timezone.now()
    hospitalization.save()

    return redirect("department:detail", department_id=department.id)

@login_required(login_url="/login/")
def transfer_patient(request, patient_id, hospitalization_id, from_department_id, to_department_id):
    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id, patient=patient)
    from_department = get_object_or_404(Department, id=from_department_id)
    to_department = get_object_or_404(Department, id=to_department_id)

    # Transfer logic
    hospitalization = Hospitalization.objects.get(patient=patient, hospitalization=hospitalization, department=from_department)
    hospitalization.department = to_department
    hospitalization.save()

    return redirect("department:detail", department_id=to_department.id)


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
            return redirect("patient:page", patient_id=patient.id)
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
            return redirect("patient:page", patient_id=patient.id)
    else:
        form = ObservationForm(instance=observation)
        
    context = {
        "form": form,
        "title" : "Edit Patient Observation",
        "patient_id" : patient.id,
    }
    
    return render(request, "patient_observation_form.html", context)