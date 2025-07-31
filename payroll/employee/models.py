from contextlib import nullcontext
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class ContractType(models.Model):
    contract_type_id = models.AutoField(primary_key=True)
    contract_type_name = models.CharField(max_length=100,null=True,blank=True,unique=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    class Meta:
        db_table = 'ContractType'

    def __str__(self):
        return self.contract_type_name

class JobTitle(models.Model):
    job_title_id = models.AutoField(primary_key=True)
    job_title_name = models.CharField(max_length=100,null=True,blank=True,unique=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'JobTitle'

    def __str__(self):
        return self.job_title_name

class Locations(models.Model):
    Location_id = models.AutoField(primary_key=True)
    Location_name= models.CharField(max_length=100,null=True,blank=True,unique=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Locations'   
    def __str__(self):
        return self.Location_name

# class Branch(models.Model):
#     branchName = models.CharField(max_length=50, unique=True, null=False,blank=False)
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=50)
#     location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True, blank=True) 
#     pincode = models.CharField(max_length=6)
#     deleted = models.BooleanField(default=False)

#     class Meta:
#         db_table = 'Branch'

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100,null=True,blank=True,unique=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Department'
    def __str__(self):
        return self.department_name

class Designation(models.Model):
    designation_name = models.CharField(max_length=50, null=False,blank=False)
    description = models.CharField(max_length=200)
   
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='department',null=True,blank=True)
    deleted = models.BooleanField(default=False)
    class Meta:
        db_table = 'Designation'
        
    def __str__(self):
        return self.designation_name


class Bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=20, blank=True, null=True,unique=True)

    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Bank'
        ordering = ['bank_name']

    def __str__(self):
        return self.bank_name

class FieldType(models.Model):
    field_type_id = models.AutoField(primary_key=True)
    field_type_name = models.CharField(max_length=100,null=True,blank=True,unique=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "field_type"
    def __str__(self):
        return self.field_type_name

class EmployeeCustomFieldConfig(models.Model):
    field_key = models.CharField(max_length=100, unique=True)  
    field_label = models.CharField(max_length=255)             
    field_type = models.ForeignKey(FieldType, on_delete=models.SET_NULL, null=True)
    is_selected = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)

    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employee_custom_field_config"

    def __str__(self):
        return self.field_label

class PhoneCountryCode(models.Model):
    code = models.CharField(max_length=10, unique=True,null=True, blank=True)   
    country = models.CharField(max_length=100,null=True, blank=True)            
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.country} ({self.code})"


User = get_user_model()
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    phone_country_code = models.ForeignKey(PhoneCountryCode, on_delete=models.DO_NOTHING,null=True, blank=True  )
    emirates_id = models.CharField(max_length=50, unique=True,null=True, blank=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    labour_card_number = models.CharField(max_length=50, blank=True, null=True)
    visa_expiry = models.DateField(blank=True, null=True)
    contract_type = models.ForeignKey(ContractType, on_delete=models.SET_NULL, null=True,related_name="employees")
    contract_start_date = models.DateField(blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    #branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)
    mohre_establishment_id = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    iban = models.CharField(max_length=50,unique=True)
    
    custom_fields = models.JSONField(blank=True, null=True)
    
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Employee'
        indexes = [
        models.Index(fields=['deleted']),
        models.Index(fields=['department']),
        models.Index(fields=['location']),
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    

# class EmployeeCustomField(models.Model):
#     employee_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
#     custom_field = models.ForeignKey(EmployeeCustomFieldConfig, on_delete=models.SET_NULL, null=True)
#     value = models.CharField(max_length=255, null=True, blank=True)
#     deleted = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
 
#     class Meta:
#         db_table = "employee_custom_field"

#     def __str__(self):
#         return self.value 
  

class Attachment(models.Model):
    document = models.URLField(null=True,blank=True)  # Changed from FileField
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='attachments',null=True,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    original_filename = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f"Attachment {self.id} for Employee {self.employee_id}"
    class Meta:
        db_table = 'attachment'
