from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .serializers import *
from .validators import *
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid
from payroll.azure_upload import *
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

####-Employee-####


User = get_user_model()

class CreateEmployeeView(APIView):
    def post(self, request):
        try:
            data = request.data
            files = request.FILES.getlist("file") 

            # Run full payload validation
            validation_result = validate_employee_payload(data)

            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })

            cleaned_data = validation_result["cleaned_data"]

            with transaction.atomic():
                phone = cleaned_data["phone_number"]

                # 1. Create user
                user = User.objects.create_user(
                    username=phone,
                    password=phone,
                    is_active=True
                )

                # 2. Create employee record
                employee = Employee.objects.create(
                    user=user,
                    first_name=cleaned_data["first_name"],
                    last_name=cleaned_data["last_name"],
                    phone_number=cleaned_data["phone_number"],
                    phone_country_code=cleaned_data.get("phone_country_code"),
                    emirates_id=cleaned_data.get("emirates_id"),
                    passport_number=cleaned_data.get("passport_number"),
                    labour_card_number=cleaned_data.get("labour_card_number"),
                    visa_expiry=cleaned_data.get("visa_expiry"),
                    contract_type=cleaned_data.get("contract_type"),
                    contract_start_date=cleaned_data.get("contract_start_date"),
                    contract_end_date=cleaned_data.get("contract_end_date"),
                    department=cleaned_data.get("department"),
                    location=cleaned_data.get("location"),
                    bank=cleaned_data.get("bank"),
                    mohre_establishment_id=cleaned_data.get("mohre_establishment_id"),
                    job_title=cleaned_data.get("job_title"),
                    iban=cleaned_data["iban"],
                    custom_fields=cleaned_data.get("custom_fields", {})
                )
                saved_attachments = []
                for file_input in files:
                    file_prefix = str(uuid.uuid4())
                    azure_url = upload_file_to_azure(file_input, folder_name="attachments", prefix=file_prefix)

                    if not azure_url:
                        raise Exception(f"File upload failed for {file_input.name}")

                    Attachment.objects.create(
                        document=azure_url,
                        employee=employee,
                        original_filename=file_input.name
                    )

                    saved_attachments.append({
                        "file_name": file_input.name,
                        "azure_url": azure_url
                    })

                return Response({
                    "message": "Employee created successfully",
                    "status": 201,
                    "attachments": saved_attachments
                })

        except ValidationError as e:
            return Response({"error": str(e), "status": 400})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateEmployeeView(APIView):
    def put(self, request, pk):
        try:
            employee = Employee.objects.get(employee_id=pk, deleted=False)
            data = request.data

            validation_result = validate_employee_payload(data)

            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })

            data = validation_result["cleaned_data"]
            
            # Update employee fields directly without validation
            for field, value in data.items():
                if hasattr(employee, field):
                    setattr(employee, field, value)
            
            employee.save()
            return Response({"message": "Employee updated successfully.", "status": 200})
            
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetEmployeeView(APIView):
    def get(self, request, pk):
        try:
            employee = Employee.objects.get(employee_id=pk, deleted=False)
            serializer = EmployeeSerializer(employee)
            return Response({"data": serializer.data, "status": 200})
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found", "status": 404})

class ListEmployeesView(APIView):
    def get(self, request):
        employees = Employee.objects.filter(deleted=False)
        serializer = EmployeeSerializer(employees, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteEmployeeView(APIView):
    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(employee_id=pk, deleted=False)
            employee.deleted = True
            employee.save()
            return Response({"message": "Employee deleted successfully.", "status": 200})
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

# Contract Type Views
class CreateContractType(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_contract_type_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                contract_type = ContractType.objects.create(**cleaned_data)
                
                return Response({
                    "id": contract_type.contract_type_id, 
                    "name": contract_type.contract_type_name,
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateContractType(APIView):
    def put(self, request, pk):
        try:
            contract_type = ContractType.objects.get(contract_type_id=pk, deleted=False)
            data = request.data
            
            # Validate payload
            validation_result = validate_contract_type_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            # Update contract type
            for field, value in cleaned_data.items():
                if hasattr(contract_type, field):
                    setattr(contract_type, field, value)
            
            contract_type.save()
            return Response({
                "message": "Contract type updated successfully.",
                "status": 200
            })
            
        except ContractType.DoesNotExist:
            return Response({"error": "Contract type not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetContractType(APIView):
    def get(self, request, pk):
        try:
            contract_type = ContractType.objects.get(contract_type_id=pk, deleted=False)
            serializer = ContractTypeSerializer(contract_type)
            return Response({"data": serializer.data, "status": 200})
        except ContractType.DoesNotExist:
            return Response({"error": "Contract type not found", "status": 404})

class ListContractTypes(APIView):
    def get(self, request):
        contract_types = ContractType.objects.filter(deleted=False)
        serializer = ContractTypeSerializer(contract_types, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteContractType(APIView):
    def delete(self, request, pk):
        try:
            contract_type = ContractType.objects.get(contract_type_id=pk, deleted=False)
            contract_type.deleted = True
            contract_type.save()
            return Response({"message": "Contract type deleted successfully.", "status": 200})
        except ContractType.DoesNotExist:
            return Response({"error": "Contract type not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

# Job Title Views
class CreateJobTitle(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_job_title_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                job_title = JobTitle.objects.create(**cleaned_data)
                
                return Response({
                    "id": job_title.job_title_id, 
                    "name": job_title.job_title_name,
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateJobTitle(APIView):
    def put(self, request, pk):
        try:
            job_title = JobTitle.objects.get(job_title_id=pk, deleted=False)
            data = request.data
            
            # Validate payload
            validation_result = validate_job_title_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            # Update job title
            for field, value in cleaned_data.items():
                if hasattr(job_title, field):
                    setattr(job_title, field, value)
            
            job_title.save()
            return Response({
                "message": "Job title updated successfully.",
                "status": 200
            })
            
        except JobTitle.DoesNotExist:
            return Response({"error": "Job title not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetJobTitle(APIView):
    def get(self, request, pk):
        try:
            job_title = JobTitle.objects.get(job_title_id=pk, deleted=False)
            serializer = JobTitleSerializer(job_title)
            return Response({"data": serializer.data, "status": 200})
        except JobTitle.DoesNotExist:
            return Response({"error": "Job title not found", "status": 404})

class ListJobTitles(APIView):
    def get(self, request):
        job_titles = JobTitle.objects.filter(deleted=False)
        serializer = JobTitleSerializer(job_titles, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteJobTitle(APIView):
    def delete(self, request, pk):
        try:
            job_title = JobTitle.objects.get(job_title_id=pk, deleted=False)
            job_title.deleted = True
            job_title.save()
            return Response({"message": "Job title deleted successfully.", "status": 200})
        except JobTitle.DoesNotExist:
            return Response({"error": "Job title not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

# Department Views
class CreateDepartment(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_department_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                department = Department.objects.create(**cleaned_data)
                
                return Response({
                    "id": department.department_id, 
                    "name": department.department_name,
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateDepartment(APIView):
    def put(self, request, pk):
        try:
            department = Department.objects.get(department_id=pk, deleted=False)
            data = request.data
            
            # Validate payload
            validation_result = validate_department_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            # Update department
            for field, value in cleaned_data.items():
                if hasattr(department, field):
                    setattr(department, field, value)
            
            department.save()
            return Response({
                "message": "Department updated successfully.",
                "status": 200
            })
            
        except Department.DoesNotExist:
            return Response({"error": "Department not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetDepartment(APIView):
    def get(self, request, pk):
        try:
            department = Department.objects.get(department_id=pk, deleted=False)
            serializer = DepartmentSerializer(department)
            return Response({"data": serializer.data, "status": 200})
        except Department.DoesNotExist:
            return Response({"error": "Department not found", "status": 404})

class ListDepartments(APIView):
    def get(self, request):
        departments = Department.objects.filter(deleted=False)
        serializer = DepartmentSerializer(departments, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteDepartment(APIView):
    def delete(self, request, pk):
        try:
            department = Department.objects.get(department_id=pk, deleted=False)
            department.deleted = True
            department.save()
            return Response({"message": "Department deleted successfully.", "status": 200})
        except Department.DoesNotExist:
            return Response({"error": "Department not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

# Branch Views
# class BranchCreateView(APIView):
#     def post(self, request):
#         serializer = BranchSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Branch created successfully.", "status": 201})
#         return Response({"error": serializer.errors, "status": 400})
# class BranchListView(APIView):
#     def get(self, request):
#         branches = Branch.objects.filter(deleted=False)
#         serializer = BranchSerializer(branches, many=True)
#         return Response({"data": serializer.data, "status": 200})
# class BranchDetailView(APIView):
#     def get(self, request, branch_id):
#         branch = get_object_or_404(Branch, id=branch_id, deleted=False)
#         serializer = BranchSerializer(branch)
#         return Response({"data": serializer.data, "status": 200})
# class BranchUpdateView(APIView):
#     def put(self, request, branch_id):
#         branch = get_object_or_404(Branch, id=branch_id, deleted=False)
#         serializer = BranchSerializer(branch, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Branch updated successfully.", "status": 200})
#         return Response({"error": serializer.errors, "status": 400})
# class BranchDeleteView(APIView):
#     def delete(self, request, branch_id):
#         branch = get_object_or_404(Branch, id=branch_id, deleted=False)
#         branch.deleted = True
#         branch.save()
#         return Response({"message": "Branch soft-deleted successfully.", "status": 204})

class DesignationCreateView(APIView):
    def post(self, request):
        serializer = DesignationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Designation created successfully.", "status": 201})
        return Response({"error": serializer.errors, "status": 400})

class DesignationListView(APIView):
    def get(self, request):
        designations = Designation.objects.filter(deleted=False)
        serializer = DesignationSerializer(designations, many=True)
        return Response({"data": serializer.data, "status": 200})

class DesignationDetailView(APIView):
    def get(self, request, designation_id):
        designation = get_object_or_404(Designation, id=designation_id, deleted=False)
        serializer = DesignationSerializer(designation)
        return Response({"data": serializer.data, "status": 200})

class DesignationUpdateView(APIView):
    def put(self, request, designation_id):
        designation = get_object_or_404(Designation, id=designation_id, deleted=False)
        serializer = DesignationSerializer(designation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Designation updated successfully.", "status": 200})
        return Response({"error": serializer.errors, "status": 400})

class DesignationDeleteView(APIView):
    def delete(self, request, designation_id):
        designation = get_object_or_404(Designation, id=designation_id, deleted=False)
        designation.deleted = True
        designation.save()
        return Response({"message": "Designation soft-deleted successfully.", "status": 204})

# Location Views
class CreateLocation(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_location_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                location = Locations.objects.create(**cleaned_data)
                
                return Response({
                    "id": location.Location_id, 
                    "name": location.Location_name,
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateLocation(APIView):
    def put(self, request, pk):
        try:
            location = Locations.objects.get(Location_id=pk, deleted=False)
            data = request.data
            
            # Validate payload
            validation_result = validate_location_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            # Update location
            for field, value in cleaned_data.items():
                if hasattr(location, field):
                    setattr(location, field, value)
            
            location.save()
            return Response({
                "message": "Location updated successfully.",
                "status": 200
            })
            
        except Locations.DoesNotExist:
            return Response({"error": "Location not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetLocation(APIView):
    def get(self, request, pk):
        try:
            location = Locations.objects.get(Location_id=pk, deleted=False)
            serializer = LocationsSerializer(location)
            return Response({"data": serializer.data, "status": 200})
        except Locations.DoesNotExist:
            return Response({"error": "Location not found", "status": 404})

class ListLocations(APIView):
    def get(self, request):
        locations = Locations.objects.filter(deleted=False)
        serializer = LocationsSerializer(locations, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteLocation(APIView):
    def delete(self, request, pk):
        try:
            location = Locations.objects.get(Location_id=pk, deleted=False)
            location.deleted = True
            location.save()
            return Response({"message": "Location deleted successfully.", "status": 200})
        except Locations.DoesNotExist:
            return Response({"error": "Location not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

# Bank Views
class CreateBank(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_bank_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                bank = Bank.objects.create(**cleaned_data)
                
                return Response({
                    "id": bank.bank_id, 
                    "name": bank.bank_name, 
                    "swift_code": bank.swift_code,
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateBank(APIView):
    def put(self, request, pk):
        try:
            bank = Bank.objects.get(bank_id=pk, deleted=False)
            data = request.data
            
            # Validate payload
            validation_result = validate_bank_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            # Update bank
            for field, value in cleaned_data.items():
                if hasattr(bank, field):
                    setattr(bank, field, value)
            
            bank.save()
            return Response({
                "message": "Bank updated successfully.",
                "status": 200
            })
            
        except Bank.DoesNotExist:
            return Response({"error": "Bank not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetBank(APIView):
    def get(self, request, pk):
        try:
            bank = Bank.objects.get(bank_id=pk, deleted=False)
            serializer = BankSerializer(bank)
            return Response({"data": serializer.data, "status": 200})
        except Bank.DoesNotExist:
            return Response({"error": "Bank not found", "status": 404})

class ListBanks(APIView):
    def get(self, request):
        banks = Bank.objects.filter(deleted=False)
        serializer = BankSerializer(banks, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteBank(APIView):
    def delete(self, request, pk):
        try:
            bank = Bank.objects.get(bank_id=pk, deleted=False)
            bank.deleted = True
            bank.save()
            return Response({"message": "Bank deleted successfully.", "status": 200})
        except Bank.DoesNotExist:
            return Response({"error": "Bank not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

# Field Type Views
class CreateFieldType(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_field_type_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                field_type = FieldType.objects.create(**cleaned_data)
                
                return Response({
                    "id": field_type.field_type_id, 
                    "name": field_type.field_type_name,
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateFieldType(APIView):
    def put(self, request, pk):
        try:
            field_type = FieldType.objects.get(field_type_id=pk, deleted=False)
            data = request.data
            
            # Validate payload
            validation_result = validate_field_type_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            # Update field type
            for field, value in cleaned_data.items():
                if hasattr(field_type, field):
                    setattr(field_type, field, value)
            
            field_type.save()
            return Response({
                "message": "Field type updated successfully.",
                "status": 200
            })
            
        except FieldType.DoesNotExist:
            return Response({"error": "Field type not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetFieldType(APIView):
    def get(self, request, pk):
        try:
            field_type = FieldType.objects.get(field_type_id=pk, deleted=False)
            serializer = FieldTypeSerializer(field_type)
            return Response({"data": serializer.data, "status": 200})
        except FieldType.DoesNotExist:
            return Response({"error": "Field type not found", "status": 404})

class ListFieldTypes(APIView):
    def get(self, request):
        field_types = FieldType.objects.filter(deleted=False)
        serializer = FieldTypeSerializer(field_types, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteFieldType(APIView):
    def delete(self, request, pk):
        try:
            field_type = FieldType.objects.get(field_type_id=pk, deleted=False)
            field_type.deleted = True
            field_type.save()
            return Response({"message": "Field type deleted successfully.", "status": 200})
        except FieldType.DoesNotExist:
            return Response({"error": "Field type not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

# Country Code Views
class CreateCountryCodeView(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_country_code_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                country_code = PhoneCountryCode.objects.create(**cleaned_data)
                
                return Response({
                    "message": "Country code created", 
                    "data": {
                        "id": country_code.id, 
                        "country": country_code.country, 
                        "code": country_code.code
                    }, 
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateCountryCodeView(APIView):
    def put(self, request, pk):
        try:
            country_code = PhoneCountryCode.objects.get(id=pk, deleted=False)
            data = request.data
            
            # Validate payload
            validation_result = validate_country_code_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            # Update country code
            for field, value in cleaned_data.items():
                if hasattr(country_code, field):
                    setattr(country_code, field, value)
            
            country_code.save()
            return Response({
                "message": "Country code updated successfully.",
                "status": 200
            })
            
        except PhoneCountryCode.DoesNotExist:
            return Response({"error": "Country code not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetCountryCodeView(APIView):
    def get(self, request, pk):
        try:
            country_code = PhoneCountryCode.objects.get(id=pk, deleted=False)
            serializer = PhoneCountryCodeCreateSerializer(country_code)
            return Response({"data": serializer.data, "status": 200})
        except PhoneCountryCode.DoesNotExist:
            return Response({"error": "Country code not found", "status": 404})

class ListCountryCodesView(APIView):
    def get(self, request):
        country_codes = PhoneCountryCode.objects.filter(deleted=False)
        serializer = PhoneCountryCodeCreateSerializer(country_codes, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteCountryCodeView(APIView):
    def delete(self, request, pk):
        try:
            country_code = PhoneCountryCode.objects.get(id=pk, deleted=False)
            country_code.deleted = True
            country_code.save()
            return Response({"message": "Country code deleted successfully.", "status": 200})
        except PhoneCountryCode.DoesNotExist:
            return Response({"error": "Country code not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class PhoneCountryCodeDropdownView(APIView):
    def get(self, request):
        codes = PhoneCountryCode.objects.filter(deleted=False)
        serializer = PhoneCountryCodeDropdownSerializer(codes, many=True)
        return Response({"data":serializer.data,"status":200})

# Custom Field Views
class CreateCustomFieldView(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_custom_field_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                custom_field = EmployeeCustomFieldConfig.objects.create(**cleaned_data)
                
                return Response({
                    "message": "Custom field created successfully.",
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class UpdateCustomFieldView(APIView):
    def put(self, request, pk):
        try:
            custom_field = EmployeeCustomFieldConfig.objects.get(id=pk, deleted=False)
            data = request.data
            
            # Validate payload
            validation_result = validate_custom_field_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            # Update custom field
            for field, value in cleaned_data.items():
                if hasattr(custom_field, field):
                    setattr(custom_field, field, value)
            
            custom_field.save()
            return Response({"message": "Custom field updated successfully.", "status": 200})
            
        except EmployeeCustomFieldConfig.DoesNotExist:
            return Response({"error": "Custom field not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetCustomFieldView(APIView):
    def get(self, request, pk):
        try:
            custom_field = EmployeeCustomFieldConfig.objects.get(id=pk, deleted=False)
            serializer = CustomFieldConfigListSerializer(custom_field)
            return Response({"data": serializer.data, "status": 200})
        except EmployeeCustomFieldConfig.DoesNotExist:
            return Response({"error": "Custom field not found", "status": 404})

class ListCustomFieldsView(APIView):
    def get(self, request):
        custom_fields = EmployeeCustomFieldConfig.objects.filter(deleted=False)
        serializer = CustomFieldConfigListSerializer(custom_fields, many=True)
        return Response({"data": serializer.data, "status": 200})

class DeleteCustomFieldView(APIView):
    def delete(self, request, pk):
        try:
            custom_field = EmployeeCustomFieldConfig.objects.get(id=pk, deleted=False)
            custom_field.deleted = True
            custom_field.save()
            return Response({"message": "Custom field deleted successfully.", "status": 200})
        except EmployeeCustomFieldConfig.DoesNotExist:
            return Response({"error": "Custom field not found", "status": 404})
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class GetSelectedCustomFieldsView(APIView):
    def get(self, request):
        """Get only selected custom fields for employee creation"""
        selected_fields = EmployeeCustomFieldConfig.objects.filter(
            is_selected=True, 
            deleted=False
        )
        serializer = CustomFieldConfigListSerializer(selected_fields, many=True)
        return Response({"data": serializer.data, "status": 200})

class CreateEmployeeCustomFieldConfig(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Validate payload
            validation_result = validate_custom_field_payload(data)
            
            if not validation_result["is_valid"]:
                return Response({
                    "status": 400,
                    "errors": validation_result["errors"]
                })
            
            cleaned_data = validation_result["cleaned_data"]
            
            with transaction.atomic():
                custom_field = EmployeeCustomFieldConfig.objects.create(**cleaned_data)
                
                return Response({
                    "id": custom_field.id,
                    "key": custom_field.field_key,
                    "label": custom_field.field_label,
                    "type": custom_field.field_type.field_type_name if custom_field.field_type else None,
                    "status": 201
                })
            
        except Exception as e:
            return Response({"error": str(e), "status": 500})

class VisaExpiryAlertView(APIView):
    

    def get(self, request):
        today = date.today()
        cutoff_date = today + timedelta(days=30)
        
        employees = Employee.objects.filter(
            visa_expiry__isnull=False,
            visa_expiry__range=(today, cutoff_date),
            deleted=False
        ).order_by('visa_expiry')

        serialized_data = EmployeeSerializer(employees, many=True).data
        return Response({
            "count": len(serialized_data),
            "employees_with_expiring_visa": serialized_data,
            "status": 200
        })

###################################################Attachement Views###################################################

class UploadAttachmentView(APIView):
    def post(self, request):
        try:
            files = request.FILES.getlist("file")  # Get all files
            employee_id = request.data.get("employee_id")

            if not files or not employee_id:
                return Response({"detail": "file(s) and employee_id are required."}, status=400)

            saved_attachments = []

            with transaction.atomic():
                for file_input in files:
                    file_prefix = str(uuid.uuid4())
                    azure_url = upload_file_to_azure(file_input, folder_name="attachments", prefix=file_prefix)

                    if not azure_url:
                        return Response({"detail": f"File upload failed for {file_input.name}."}, status=500)

                    attachment = Attachment.objects.create(
                        document=azure_url,
                        employee_id=employee_id,
                        original_filename=file_input.name
                    )

                    saved_attachments.append({
                        "original_filename": file_input.name,
                        "employee_id": int(employee_id),
                        "document_url": azure_url,
                        "created_at": now()
                        # "created_by_id": request.user.id if needed
                    })

            return Response({"attachments": saved_attachments}, status=201)

        except Exception as e:
            return Response({"detail": str(e)}, status=500)

           
class GetAttachmentView(APIView):
    def get(self, request, pk):
        attachment = get_object_or_404(Attachment, pk=pk)
        return Response(AttachmentSerializer(attachment).data)

class ListAttachmentsView(APIView):
    def get(self, request, pk):
        attachments = Attachment.objects.filter(lead_id=pk)

        return Response({
            "count": attachments.count(),
            "results": AttachmentSerializer(attachments, many=True).data
        })
class DeleteAttachmentView(APIView):
    def delete(self, request, pk):
        attachment = get_object_or_404(Attachment, pk=pk)
        attachment.delete()
        return Response({"detail": "Deleted successfully."}, status=204)






