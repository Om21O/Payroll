from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ContractType)
admin.site.register(JobTitle)
admin.site.register(Department)
admin.site.register(Locations)
admin.site.register(Bank)
admin.site.register(FieldType)
admin.site.register(EmployeeCustomFieldConfig)
admin.site.register(Employee)
#admin.site.register(EmployeeCustomField)
admin.site.register(PhoneCountryCode)