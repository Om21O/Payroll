from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from django.db import IntegrityError

class EmployeeSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Employee
        fields = "__all__"

class ContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractType
        fields = "__all__"

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = "__all__"

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"

class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = "__all__"

class PhoneCountryCodeDropdownSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='code')

    class Meta:
        model = PhoneCountryCode
        fields = ['id', 'value']

class PhoneCountryCodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneCountryCode
        fields = ["country", "code"]

class CreateCustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCustomFieldConfig
        fields = "__all__"

# class EmployeeCustomFieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployeeCustomField
#         fields = "__all__"

# New serializer for getting custom field configurations
class CustomFieldConfigListSerializer(serializers.ModelSerializer):
    field_type_name = serializers.CharField(source='field_type.field_type_name', read_only=True)
    
    class Meta:
        model = EmployeeCustomFieldConfig
        fields = '__all__'
    
# class BranchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Branch
#         fields = '__all__'



class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
        read_only_fields = ['uploaded_at', 'original_filename', 'file_size']