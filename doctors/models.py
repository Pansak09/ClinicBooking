from django.db import models

class Doctor(models.Model):
    name      = models.CharField("ชื่อแพทย์", max_length=100)
    specialty = models.CharField("สาขา", max_length=100)
    contact   = models.CharField("เบอร์ติดต่อ", max_length=50, blank=True)
    address   = models.TextField("ที่อยู่", blank=True)
    image     = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DoctorCheckin(models.Model):
    doctor      = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="แพทย์")
    checkin_at = models.DateTimeField("วันที่เข้าทำงาน", blank=True, null=True)
    note        = models.TextField("หมายเหตุ", blank=True)

    def __str__(self):
        return f"{self.doctor.name} ({self.checkin_at})"