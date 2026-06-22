from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from doctors.models import Doctor

@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related('doctor').order_by('-appointment_time')
    return render(request, 'appointments/list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        appointment = form.save()
        messages.success(request, f"เพิ่มนัดหมายของ {appointment.patient_name} สำเร็จ!")
        return redirect('appointments:list')
    return render(request, 'appointments/form.html', {'form': form})

@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        messages.success(request, f"✏️ อัปเดตข้อมูลของ {appointment.patient_name} เรียบร้อยแล้ว!")
        return redirect('appointments:list')
    return render(request, 'appointments/form.html', {'form': form})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.warning(request, f"🗑️ ลบนัดหมายของ {appointment.patient_name} สำเร็จ!")
        return redirect('appointments:list')
    return render(request, 'appointments/confirm_delete.html', {'appointment': appointment})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/detail.html', {'appointment': appointment})

@login_required
def appointment_update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        status_order = {
            'pending': 'completed',
            'completed': 'canceled',
            'canceled': 'pending'
        }
        appointment.status = status_order.get(appointment.status, 'pending')
        appointment.save()
        messages.success(request, f"อัปเดตสถานะของ {appointment.patient_name} เป็น {appointment.get_status_display()} สำเร็จ!")

    return redirect('appointments:list')

@login_required
def home(request):
    total_appointments = Appointment.objects.count()
    pending_count = Appointment.objects.filter(status='pending').count()
    completed_count = Appointment.objects.filter(status='completed').count()
    total_doctors = Doctor.objects.count()

    context = {
        'total_appointments': total_appointments,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'total_doctors': total_doctors,
    }
    return render(request, 'home.html', context)
