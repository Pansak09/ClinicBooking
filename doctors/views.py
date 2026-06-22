from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, DoctorCheckin
from .forms import DoctorForm, DoctorCheckinForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from appointments.models import Appointment

@login_required
def home_view(request):
    """หน้า Dashboard หลัก"""
    #นับจำนัดหมายทั้งหมด
    total_appointments = Appointment.objects.count()
    #นับค่าสถานะ รอพบแพทย์
    pending_count = Appointment.objects.filter(status="pending").count()
    #นับสถานะ เสร็จสิ้น
    completed_count = Appointment.objects.filter(status="completed").count()
    
    #เก็บค่าสถานะ
    context = {
        "total_appointments": total_appointments,
        "pending_count": pending_count,
        "completed_count": completed_count,
    }
    return render(request, "home.html", context) #ส่งใปแสดง

def doctor_list(request):
    #ดึงข้อมูลแพทย์ทั้งหมดจากฐานข้อมูล
    doctors = Doctor.objects.all().order_by('-created_at')
    #ลูป ตรวจสอบการเช็คชื่อเข้าเวร
    for doctor in doctors:
        #ดึง record ล่าสุด
        checkin = DoctorCheckin.objects.filter(doctor=doctor).order_by('-checkin_at').first()
        doctor.latest_checkin = checkin.checkin_at if checkin else None
    return render(request, 'doctors/list.html', {'doctors': doctors})


def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        checkin_form = DoctorCheckinForm(request.POST)
        if form.is_valid() and checkin_form.is_valid():
            doctor = form.save()
            checkin = checkin_form.save(commit=False)
            checkin.doctor = doctor
            checkin.save()
            return redirect('doctors:list')
    else:
        form = DoctorForm()
        checkin_form = DoctorCheckinForm()
    return render(request, 'doctors/form.html', {
        'form': form,
        'checkin_form': checkin_form
    })

def doctor_update(request, pk):
    #ดึงแพทย์ตาม pk 
    doctor = get_object_or_404(Doctor, pk=pk)
    checkin, created = DoctorCheckin.objects.get_or_create(doctor=doctor)

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        checkin_form = DoctorCheckinForm(request.POST, instance=checkin)
        if form.is_valid() and checkin_form.is_valid():
            form.save()
            checkin_form.save()
            return redirect('doctors:list')
    else:
        form = DoctorForm(instance=doctor)
        checkin_form = DoctorCheckinForm(instance=checkin)
    
    return render(request, 'doctors/form.html', {
        'form': form,
        'checkin_form': checkin_form
    })


def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctors:list')
    return render(request, 'doctors/confirm_delete.html', {'doctor': doctor})

def doctor_checkin_edit(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    checkin, created = DoctorCheckin.objects.get_or_create(doctor=doctor)

    form = DoctorCheckinForm(request.POST or None, instance=checkin)
    if request.method == 'POST' and form.is_valid():
        #ถ้าข้อมูลถูกต้องบันทึก
        form.save()
        return redirect('doctors:list')
    
    #ถ้าเป็น get แสดง
    return render(request, 'doctors/checkin_form.html', {'form': form, 'doctor': doctor})