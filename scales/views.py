
from django.shortcuts import redirect, render, get_object_or_404

from . models import NortonScale
from . forms import NortonScaleForm
from patient.models import Patient


def add_norton_scale(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    
    if request.method == "POST":
        form = NortonScaleForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            scale = form.save(commit=False)
            scale.created_by = request.user
            scale.patient = patient
            scale.save()
            return redirect("patient:page", pk=patient.id)
        else:
            print(form.errors)
    else:
        form = NortonScaleForm()
        
    context = {
        "form" : form, 
        "title" : "Add Norton Scale",
        "patient_id" : patient.id,
    }
    
    return render(request,"norton_form_create.html", context)

def edit_norton_scale(request, patient_id, norton_id):
    patient = get_object_or_404(Patient, id= patient_id)
    norton = get_object_or_404(NortonScale, id=norton_id, patient=patient)
    
    if request.method == "POST":
        form = NortonScaleForm(request.POST, instance=norton)
        if form.is_valid():
            form.save()
            return redirect("patient:page", pk=patient.id)
    else:
        form = NortonScaleForm(instance=norton)
        
    context = {
        "form": form,
        "title" : "Edit Norton Scale",
        "patient_id" : patient.id,
    }
    
    return render(request,"norton_form_create.html", context)
            
            
    