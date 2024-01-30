
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import NortonScale, GlasgowComaScale, NewsScale
from . forms import NortonScaleForm, GlasgowComaScaleForm, NewsScaleForm
from patient.models import Patient

@login_required(login_url = "/login/")
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
    
    return render(request,"scale_form.html", context)

@login_required(login_url = "/login/")
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
    
    return render(request,"scale_form.html", context)

@login_required(login_url = "/login/")
def add_glasgow_scale(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    
    if request.method == "POST":
        form = GlasgowComaScaleForm(request.POST)
        if form.is_valid():
            scale = form.save(commit=False)
            scale.created_by = request.user
            scale.patient = patient
            scale.save()
            return redirect("patient:page", pk=patient.id)
        else:
            print(form.errors)
    else:
        form = GlasgowComaScaleForm()
        
    context = {
        "form" : form,
        "title" : "Add Glasgow Coma Scale",
        "patient_id" : patient.id,
    }
    
    return render(request, "scale_form.html", context)

@login_required(login_url = "/login/")
def edit_glasgow_scale(request, patient_id, glasgow_id):
    patient = get_object_or_404(Patient, id=patient_id)
    glasgow = get_object_or_404(GlasgowComaScale, id=glasgow_id, patient=patient)
    
    if request.method == "POST":
        form = GlasgowComaScaleForm(request.POST, instance=glasgow)
        if form.is_valid():
            form.save()
            return redirect("patient:page", pk=patient.id)
    else:
        form = GlasgowComaScaleForm(instance=glasgow)
        
    context = {
        "form" : form,
        "title" : "Edit Glasgow Coma Scale",
        "patient_id" : patient.id,
    }
    
    return render(request, "scale_form.html", context)
        
def add_news_scale(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    
    if request.method == "POST":
        form = NewsScaleForm(request.POST)
        if form.is_valid():
            scale = form.save(commit=False)
            scale.created_by = request.user
            scale.patient = patient
            scale.save()
            return redirect("patient:page", pk=patient.id)
        else:
            print(form.errors)
    else:
        form = NewsScaleForm()
        
    context = {
        "form" : form,
        "title" : "Add National Early Warning Score",
        "patient_id" : patient.id,
    }
    
    return render(request, "glasgow_form.html", context)

def edit_news_scale(request, patient_id, news_id):
    patient = get_object_or_404(Patient, id=patient_id)
    news = get_object_or_404(NewsScale, id=news_id, patient=patient)
    
    if request.method == "POST":
        form = NewsScaleForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect("patient:page", pk=patient.id)
    else:
        form = NewsScaleForm(instance=news)
        
         
    context = {
        "form" : form,
        "title" : "Add National Early Warning Score",
        "patient_id" : patient.id,
    }
    
    return render(request, "glasgow_form.html", context)
            
            
    