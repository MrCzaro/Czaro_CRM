from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth.decorators import login_required



from django.utils import timezone
from .models import Department, Hospitalization
from .forms import DepartmentForm
from patient.models import Patient
from visit.models import Visit


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
    admitted_patients = Visit.objects.filter(
        is_discharged=False,
        department=department  # Assuming you have a ForeignKey from Visit to Department
    )

    context = {
        "department": department,
        "admitted_patients": admitted_patients,
        "title": "Admitted Patients",
    }

    return render(request, "admitted_patients.html", context)

@login_required(login_url="/login/")
def admit_patient(request, patient_id, visit_id, department_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visit = get_object_or_404(Visit, id=visit_id, patient=patient)
    department = get_object_or_404(Department, id=department_id)
    
    # Check if the patient is already admitted in another department for the same visit:
    if Hospitalization.objects.filter(patient=patient, visit=visit).exists():
        context = {
            "title" : "Admission Error",
            "patient" : patient,
            "visit" : visit,
        }
        
        return render(request, "admit_error.html", context)
    # Admission logic
    hospitalization = Hospitalization(patient=patient, visit=visit, department=department)
    hospitalization.save()
    
    return redirect("department:detail", department_id=department.id)

    

@login_required(login_url="/login/")
def discharge_patient(request, patient_id, visit_id, department_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visit = get_object_or_404(Visit, id=visit_id, patient=patient)
    department = get_object_or_404(Department, id=department_id)

    # Discharge logic
    hospitalization = Hospitalization.objects.get(patient=patient, visit=visit, department=department)
    hospitalization.discharged_on = timezone.now()
    hospitalization.save()

    return redirect("department:detail", department_id=department.id)

@login_required(login_url="/login/")
def transfer_patient(request, patient_id, visit_id, from_department_id, to_department_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visit = get_object_or_404(Visit, id=visit_id, patient=patient)
    from_department = get_object_or_404(Department, id=from_department_id)
    to_department = get_object_or_404(Department, id=to_department_id)

    # Transfer logic
    hospitalization = Hospitalization.objects.get(patient=patient, visit=visit, department=from_department)
    hospitalization.department = to_department
    hospitalization.save()

    return redirect("department:detail", department_id=to_department.id)