from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor
from datetime import timedelta

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending',   'รอพบแพทย์'),
        ('completed', 'เสร็จสิ้น'),
        ('canceled',  'ยกเลิก'),
    ]

    GENDER_CHOICES = [
        ('male', 'ชาย'),
        ('female', 'หญิง'),
        ('other', 'อื่น ๆ'),
    ]

    patient_name     = models.CharField("ชื่อผู้ป่วย", max_length=100)
    patient_phone    = models.CharField("เบอร์โทรผู้ป่วย", max_length=15, blank=True, null=True)
    gender           = models.CharField("เพศ", max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    age              = models.PositiveIntegerField("อายุ (ปี)", blank=True, null=True)
    weight           = models.DecimalField("น้ำหนัก (กก.)", max_digits=5, decimal_places=2, blank=True, null=True)
    height           = models.DecimalField("ส่วนสูง (ซม.)", max_digits=5, decimal_places=2, blank=True, null=True)
    symptoms         = models.TextField("อาการเบื้องต้น", blank=True, null=True)
    underlying_disease = models.CharField("โรคประจำตัว", max_length=255, blank=True, null=True)
    allergies        = models.CharField("ประวัติการแพ้ยา/อาหาร", max_length=255, blank=True, null=True)

    doctor           = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="แพทย์")
    appointment_time = models.DateTimeField("วันเวลานัดหมาย")
    description      = models.TextField("หมายเหตุเพิ่มเติม", blank=True, null=True)
    status           = models.CharField("สถานะ", max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name} ({self.get_status_display()})"

    def get_status_display_color(self):
        colors = {
            'pending': 'warning',
            'completed': 'success',
            'canceled': 'danger',
        }
        return colors.get(self.status, 'secondary')
