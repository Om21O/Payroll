from django.urls import path
from .views import *

urlpatterns = [
    # Employee CRUD
    path("create_employee/", CreateEmployeeView.as_view(), name="create_employee"),
    path("update_employee/<int:pk>/", UpdateEmployeeView.as_view(), name="update_employee"),
    path("get_employee/<int:pk>/", GetEmployeeView.as_view(), name="get_employee"),
    path("list_employees/", ListEmployeesView.as_view(), name="list_employees"),
    path("delete_employee/<int:pk>/", DeleteEmployeeView.as_view(), name="delete_employee"),

    # Contract Type CRUD
    path("create_contract_type/", CreateContractType.as_view(), name="create_contract_type"),
    path("update_contract_type/<int:pk>/", UpdateContractType.as_view(), name="update_contract_type"),
    path("get_contract_type/<int:pk>/", GetContractType.as_view(), name="get_contract_type"),
    path("list_contract_types/", ListContractTypes.as_view(), name="list_contract_types"),
    path("delete_contract_type/<int:pk>/", DeleteContractType.as_view(), name="delete_contract_type"),

    # Job Title CRUD
    path("create_job_title/", CreateJobTitle.as_view(), name="create_job_title"),
    path("update_job_title/<int:pk>/", UpdateJobTitle.as_view(), name="update_job_title"),
    path("get_job_title/<int:pk>/", GetJobTitle.as_view(), name="get_job_title"),
    path("list_job_titles/", ListJobTitles.as_view(), name="list_job_titles"),
    path("delete_job_title/<int:pk>/", DeleteJobTitle.as_view(), name="delete_job_title"),

    # Department CRUD
    path("create_department/", CreateDepartment.as_view(), name="create_department"),
    path("update_department/<int:pk>/", UpdateDepartment.as_view(), name="update_department"),
    path("get_department/<int:pk>/", GetDepartment.as_view(), name="get_department"),
    path("list_departments/", ListDepartments.as_view(), name="list_departments"),
    path("delete_department/<int:pk>/", DeleteDepartment.as_view(), name="delete_department"),

    # Location CRUD
    path("create_location/", CreateLocation.as_view(), name="create_location"),
    path("update_location/<int:pk>/", UpdateLocation.as_view(), name="update_location"),
    path("get_location/<int:pk>/", GetLocation.as_view(), name="get_location"),
    path("list_locations/", ListLocations.as_view(), name="list_locations"),
    path("delete_location/<int:pk>/", DeleteLocation.as_view(), name="delete_location"),

    # Bank CRUD
    path("create_bank/", CreateBank.as_view(), name="create_bank"),
    path("update_bank/<int:pk>/", UpdateBank.as_view(), name="update_bank"),
    path("get_bank/<int:pk>/", GetBank.as_view(), name="get_bank"),
    path("list_banks/", ListBanks.as_view(), name="list_banks"),
    path("delete_bank/<int:pk>/", DeleteBank.as_view(), name="delete_bank"),

    # Field Type CRUD
    path("create_field_type/", CreateFieldType.as_view(), name="create_field_type"),
    path("update_field_type/<int:pk>/", UpdateFieldType.as_view(), name="update_field_type"),
    path("get_field_type/<int:pk>/", GetFieldType.as_view(), name="get_field_type"),
    path("list_field_types/", ListFieldTypes.as_view(), name="list_field_types"),
    path("delete_field_type/<int:pk>/", DeleteFieldType.as_view(), name="delete_field_type"),

    # Phone Country Code CRUD
    path("create_country_code/", CreateCountryCodeView.as_view(), name="create_country_code"),
    path("update_country_code/<int:pk>/", UpdateCountryCodeView.as_view(), name="update_country_code"),
    path("get_country_code/<int:pk>/", GetCountryCodeView.as_view(), name="get_country_code"),
    path("list_country_codes/", ListCountryCodesView.as_view(), name="list_country_codes"),
    path("delete_country_code/<int:pk>/", DeleteCountryCodeView.as_view(), name="delete_country_code"),
    path("phone_country_code_dropdown/", PhoneCountryCodeDropdownView.as_view(), name="phone_country_code_dropdown"),

    # Custom Field CRUD
    path("create_custom_field/", CreateCustomFieldView.as_view(), name="create_custom_field"),
    path("update_custom_field/<int:pk>/", UpdateCustomFieldView.as_view(), name="update_custom_field"),
    path("get_custom_field/<int:pk>/", GetCustomFieldView.as_view(), name="get_custom_field"),
    path("list_custom_fields/", ListCustomFieldsView.as_view(), name="list_custom_fields"),
    path("delete_custom_field/<int:pk>/", DeleteCustomFieldView.as_view(), name="delete_custom_field"),
    path("get_selected_custom_fields/", GetSelectedCustomFieldsView.as_view(), name="get_selected_custom_fields"),

    # Employee Custom Field Config
    path("create_employee_custom_field/", CreateEmployeeCustomFieldConfig.as_view(), name="create_employee_custom_field"),

    # Visa Expiry Alert
    path("visa_expiry_alert/", VisaExpiryAlertView.as_view(), name="visa_expiry_alert"),

    # # Branch Views
    # path("create_branch/", BranchCreateView.as_view(), name="create_branch"),
    # path("list_branches/", BranchListView.as_view(), name="list_branches"),
    # path("get_branch/<int:branch_id>/", BranchDetailView.as_view(), name="get_branch"),
    # path("update_branch/<int:branch_id>/", BranchUpdateView.as_view(), name="update_branch"),
    # path("delete_branch/<int:branch_id>/", BranchDeleteView.as_view(), name="delete_branch"),
    
    # Designation Views
    path("create_designation/", DesignationCreateView.as_view(), name="create_designation"),
    path("list_designations/", DesignationListView.as_view(), name="list_designations"),
    path("get_designation/<int:designation_id>/", DesignationDetailView.as_view(), name="get_designation"),
    path("update_designation/<int:designation_id>/", DesignationUpdateView.as_view(), name="update_designation"),
    path("delete_designation/<int:designation_id>/", DesignationDeleteView.as_view(), name="delete_designation"),   

    # Attachment Views
    path("upload_attachment/", UploadAttachmentView.as_view(), name="upload_attachment"),
    path("get_attachment/<int:pk>/", GetAttachmentView.as_view(), name="get_attachment"),
    path("list_attachments/", ListAttachmentsView.as_view(), name="list_attachments"),
    path("delete_attachment/<int:pk>/", DeleteAttachmentView.as_view(), name="delete_attachment"),


]