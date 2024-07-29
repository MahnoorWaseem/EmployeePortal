from django.db import models

# Create your models here.
class EmpInfo(models.Model):
    eid=models.CharField(primary_key=True,max_length=30)
    ename=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    address=models.CharField(max_length=30)
    salary=models.CharField(max_length=30)
    # dept=models.CharField(max_length=30,default='')
    # pic=models.FileField(default='')
    image = models.ImageField(upload_to='images', default='',null=True)  
    dept=models.CharField(max_length=30,default='',null=True)
    designation=models.CharField(max_length=30,default='')

    class Meta:  
        db_table = "empInfo" 




class Attendance(models.Model):
    eid=models.ForeignKey(EmpInfo, on_delete=models.CASCADE)
    date=models.CharField(max_length=30)
    timein=models.CharField(max_length=30,null=True)
    timeout=models.CharField(max_length=30,null=True, blank=True)
    workinghr=models.CharField(max_length=30,default='',null=True)
    class Meta:
        db_table="attendance"

# class admininfo(models.Model):
#     eid=models.CharField(max_length=10)
#     ename=models.CharField(max_length=30)
#     email=models.EmailField()
#     password2=models.CharField(max_length=10)
#     image=models.CharField(max_length=30)
#     designation=models.CharField(max_length=10)
#     class Meta:
#        managed = False

class Admininfo(models.Model):
    eid = models.CharField(primary_key=True, max_length=10)
    ename = models.CharField(max_length=30)
    email = models.CharField(max_length=20)
    password2 = models.CharField(max_length=10, blank=True, null=True)
    image = models.CharField(max_length=30, blank=True, null=True)
    designation = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admininfo'


