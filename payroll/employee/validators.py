from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import *
import re
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

def validate_uae_iban(iban):
    """Validate UAE IBAN format and structure"""
    if not iban:
        return False, "IBAN is required."
    
    # Remove spaces and convert to uppercase
    iban = iban.replace(' ', '').upper()
    
    # UAE IBAN format: AE + 2 digits + 3 letters + 16 digits = 23 characters total
    if len(iban) != 23:
        return False, "UAE IBAN must be exactly 23 characters long."
    
    # Check country code (must be AE for UAE)
    if not iban.startswith('AE'):
        return False, "IBAN must start with 'AE' for UAE banks."
    
    # Check format: AE + 2 digits + 3 letters + 16 digits
    if not re.match(r'^AE[0-9]{2}[A-Z]{3}[0-9]{16}$', iban):
        return False, "Invalid UAE IBAN format. Expected: AE + 2 digits + 3 letters + 16 digits"
    
    # Validate UAE bank codes (common UAE bank codes)
    uae_bank_codes = [
        'SCBL',  # Standard Chartered Bank
        'EBIL',  # Emirates NBD
        'ADCB',  # Abu Dhabi Commercial Bank
        'DUBB',  # Dubai Islamic Bank
        'FGBB',  # First Gulf Bank
        'NBAD',  # National Bank of Abu Dhabi
        'RAKB',  # RAK Bank
        'MASH',  # Mashreq Bank
        'HSBC',  # HSBC Bank
        'CITI',  # Citibank
        'ABUD',  # Abu Dhabi Islamic Bank
        'UNBD',  # Union National Bank
        'AJMB',  # Ajman Bank
        'SHAR',  # Sharjah Islamic Bank
        'ENBD',  # Emirates NBD (alternative)
        'ADIB',  # Abu Dhabi Islamic Bank (alternative)
        'DIB',   # Dubai Islamic Bank (alternative)
        'FAB',   # First Abu Dhabi Bank
        'CBD',   # Commercial Bank of Dubai
        'NBF',   # National Bank of Fujairah
    ]
    
    bank_code = iban[4:8]  # Extract bank code (positions 5-8)
    if bank_code not in uae_bank_codes:
        return False, f"Invalid UAE bank code '{bank_code}'. Please check the bank code in your IBAN."
    
    # Validate check digits (positions 3-4)
    check_digits = iban[2:4]
    if not check_digits.isdigit():
        return False, "Check digits must be numeric."
    
    # Additional validation: Account number should not be all zeros
    account_number = iban[8:]
    if account_number == '0' * 16:
        return False, "Account number cannot be all zeros."
    
    return True, "Valid UAE IBAN"

# def validate_international_iban(iban):
#     """Validate international IBAN format and checksum"""
#     if not iban:
#         return False, "IBAN is required."
    
#     # Remove spaces and convert to uppercase
#     iban = iban.replace(' ', '').upper()
    
#     # Check minimum and maximum length (IBANs range from 15 to 34 characters)
#     if len(iban) < 15 or len(iban) > 34:
#         return False, f"IBAN length must be between 15 and 34 characters. Current length: {len(iban)}"
    
#     # Check country code format (2 letters)
#     if not re.match(r'^[A-Z]{2}[0-9A-Z]+$', iban):
#         return False, "IBAN must start with 2 letters (country code) followed by alphanumeric characters."
    
#     # Extract country code
#     country_code = iban[:2]
    
#     # Define IBAN lengths for different countries
#     iban_lengths = {
#         'AD': 24, 'AE': 23, 'AL': 28, 'AT': 20, 'AZ': 28, 'BA': 20, 'BE': 16, 'BG': 22,
#         'BH': 22, 'BR': 29, 'CH': 21, 'CR': 21, 'CY': 28, 'CZ': 24, 'DE': 22, 'DK': 18,
#         'DO': 28, 'EE': 20, 'ES': 24, 'FI': 18, 'FO': 18, 'FR': 27, 'GB': 22, 'GE': 22,
#         'GI': 23, 'GL': 18, 'GR': 27, 'GT': 28, 'HR': 21, 'HU': 28, 'IE': 22, 'IL': 23,
#         'IS': 26, 'IT': 27, 'JO': 30, 'KW': 30, 'KZ': 20, 'LB': 28, 'LI': 21, 'LT': 20,
#         'LU': 20, 'LV': 21, 'MC': 27, 'MD': 24, 'ME': 22, 'MK': 19, 'MR': 27, 'MT': 31,
#         'MU': 30, 'NL': 18, 'NO': 15, 'PK': 24, 'PL': 28, 'PS': 29, 'PT': 25, 'QA': 29,
#         'RO': 24, 'RS': 22, 'SA': 24, 'SE': 24, 'SI': 19, 'SK': 24, 'SM': 27, 'TN': 24,
#         'TR': 26, 'VG': 24, 'XK': 20
#     }
    
#     # Check if country code is supported and length is correct
#     if country_code in iban_lengths:
#         expected_length = iban_lengths[country_code]
#         if len(iban) != expected_length:
#             return False, f"IBAN for {country_code} must be {expected_length} characters long. Current length: {len(iban)}"
#     else:
#         # For unsupported countries, just check basic format
#         if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]?){0,16}$', iban):
#             return False, f"Invalid IBAN format for country {country_code}."
    
#     # Validate IBAN checksum (MOD-97 algorithm)
#     if not validate_iban_checksum(iban):
#         return False, "Invalid IBAN checksum. Please check the IBAN number."
    
#     return True, f"Valid IBAN for {country_code}"

def validate_iban_checksum(iban):
    """Validate IBAN using MOD-97 algorithm"""
    # Move first 4 characters to end: ABCD1234... -> 1234...ABCD
    iban_rearranged = iban[4:] + iban[:4]
    
    # Convert letters to numbers: A=10, B=11, ..., Z=35
    iban_numeric = ''
    for char in iban_rearranged:
        if char.isdigit():
            iban_numeric += char
        else:
            iban_numeric += str(ord(char) - ord('A') + 10)
    
    # Calculate modulo 97
    remainder = int(iban_numeric) % 97
    
    # Valid IBAN should have remainder = 1
    return remainder == 1

def validate_employee_payload(data):
    """Validate employee creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required text fields
    for field in ["first_name", "last_name", "phone_number"]:
        value = data.get(field)
        if not value:
            errors[field] = f"{field.replace('_', ' ').capitalize()} is required."
        else:
            cleaned_data[field] = value

    # IBAN validation - Choose between UAE and International validation
    iban = data.get("iban")
    if not iban:
        errors["iban"] = "IBAN is required."
    else:
        # Option 1: Use UAE IBAN validation (commented out)
        is_valid_iban, iban_error = validate_uae_iban(iban)
        
        # Option 2: Use International IBAN validation (currently active)
        #is_valid_iban, iban_error = validate_international_iban(iban)
        
        if not is_valid_iban:
            errors["iban"] = iban_error
        else:
            cleaned_data["iban"] = iban

    # PhoneCountryCode (FK)
    phone_code_id = data.get("phone_country_code")
    if phone_code_id:
        try:
            cleaned_data["phone_country_code"] = PhoneCountryCode.objects.get(id=phone_code_id)
        except ObjectDoesNotExist:
            errors["phone_country_code"] = f"PhoneCountryCode with id {phone_code_id} does not exist."

    # Payroll Mandatory Fields - Required for payroll inclusion
    payroll_mandatory_fields = ["emirates_id", "labour_card_number", "mohre_establishment_id"]
    for field in payroll_mandatory_fields:
        value = data.get(field)
        if not value:
            errors[field] = f"{field.replace('_', ' ').capitalize()} is mandatory for payroll inclusion."
        else:
            cleaned_data[field] = value

    # Optional passport
    passport_number = data.get("passport_number")
    if passport_number:
        cleaned_data["passport_number"] = passport_number

    # Dates
    for field in ["visa_expiry", "contract_start_date", "contract_end_date"]:
        value = data.get(field)
        if value:
            try:
                parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
                cleaned_data[field] = parsed_date
                
                # Special validation for visa expiry date
                if field == "visa_expiry":
                    from datetime import date, timedelta
                    today = date.today()
                    thirty_days_from_now = today + timedelta(days=30)
                    
                    if parsed_date <= thirty_days_from_now:
                        errors[field] = f"Visa expires in next 30 days. Expiry date: {parsed_date}, Current date: {today}"
                        
            except ValueError:
                errors[field] = f"{field.replace('_', ' ').capitalize()} must be in YYYY-MM-DD format."

    # ContractType FK
    contract_type_id = data.get("contract_type")
    if contract_type_id:
        try:
            cleaned_data["contract_type"] = ContractType.objects.get(id=contract_type_id)
        except ObjectDoesNotExist:
            errors["contract_type"] = f"ContractType with id {contract_type_id} does not exist."

    # Department FK
    department_id = data.get("department")
    if department_id:
        try:
            cleaned_data["department"] = Department.objects.get(id=department_id)
        except ObjectDoesNotExist:
            errors["department"] = f"Department with id {department_id} does not exist."

    # Location FK
    location_id = data.get("location")
    if location_id:
        try:
            cleaned_data["location"] = Locations.objects.get(id=location_id)
        except ObjectDoesNotExist:
            errors["location"] = f"Location with id {location_id} does not exist."

    # Bank FK
    bank_id = data.get("bank")
    if bank_id:
        try:
            cleaned_data["bank"] = Bank.objects.get(id=bank_id)
        except ObjectDoesNotExist:
            errors["bank"] = f"Bank with id {bank_id} does not exist."

    # Job Title FK
    job_title_id = data.get("job_title")
    if job_title_id:
        try:
            cleaned_data["job_title"] = JobTitle.objects.get(id=job_title_id)
        except ObjectDoesNotExist:
            errors["job_title"] = f"JobTitle with id {job_title_id} does not exist."

    # JSON field: custom_fields
    custom_fields = data.get("custom_fields")
    if custom_fields:
        if isinstance(custom_fields, dict):
            cleaned_data["custom_fields"] = custom_fields
        else:
            errors["custom_fields"] = "custom_fields must be a JSON object."

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }

def validate_contract_type_payload(data):
    """Validate contract type creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required field
    contract_type_name = data.get("contract_type_name")
    if not contract_type_name:
        errors["contract_type_name"] = "Contract type name is required."
    else:
        # Check uniqueness
        existing = ContractType.objects.filter(
            contract_type_name=contract_type_name, 
            deleted=False
        )
        if existing.exists():
            errors["contract_type_name"] = "Contract type name already exists."
        else:
            cleaned_data["contract_type_name"] = contract_type_name

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }

def validate_job_title_payload(data):
    """Validate job title creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required field
    job_title_name = data.get("job_title_name")
    if not job_title_name:
        errors["job_title_name"] = "Job title name is required."
    else:
        # Check uniqueness
        existing = JobTitle.objects.filter(
            job_title_name=job_title_name, 
            deleted=False
        )
        if existing.exists():
            errors["job_title_name"] = "Job title name already exists."
        else:
            cleaned_data["job_title_name"] = job_title_name

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }

def validate_department_payload(data):
    """Validate department creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required field
    department_name = data.get("department_name")
    if not department_name:
        errors["department_name"] = "Department name is required."
    else:
        # Check uniqueness
        existing = Department.objects.filter(
            department_name=department_name, 
            deleted=False
        )
        if existing.exists():
            errors["department_name"] = "Department name already exists."
        else:
            cleaned_data["department_name"] = department_name

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }

def validate_location_payload(data):
    """Validate location creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required field
    location_name = data.get("Location_name")
    if not location_name:
        errors["Location_name"] = "Location name is required."
    else:
        # Check uniqueness
        existing = Locations.objects.filter(
            Location_name=location_name, 
            deleted=False
        )
        if existing.exists():
            errors["Location_name"] = "Location name already exists."
        else:
            cleaned_data["Location_name"] = location_name

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }

def validate_bank_payload(data):
    """Validate bank creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required field
    bank_name = data.get("bank_name")
    if not bank_name:
        errors["bank_name"] = "Bank name is required."
    else:
        # Check uniqueness
        existing = Bank.objects.filter(
            bank_name=bank_name, 
            deleted=False
        )
        if existing.exists():
            errors["bank_name"] = "Bank name already exists."
        else:
            cleaned_data["bank_name"] = bank_name

    # Optional swift code
    swift_code = data.get("swift_code")
    if swift_code:
        # Check uniqueness
        existing = Bank.objects.filter(
            swift_code=swift_code, 
            deleted=False
        )
        if existing.exists():
            errors["swift_code"] = "Swift code already exists."
        else:
            cleaned_data["swift_code"] = swift_code

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }

def validate_field_type_payload(data):
    """Validate field type creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required field
    field_type_name = data.get("field_type_name")
    if not field_type_name:
        errors["field_type_name"] = "Field type name is required."
    else:
        # Check uniqueness
        existing = FieldType.objects.filter(
            field_type_name=field_type_name, 
            deleted=False
        )
        if existing.exists():
            errors["field_type_name"] = "Field type name already exists."
        else:
            cleaned_data["field_type_name"] = field_type_name

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }

def validate_country_code_payload(data):
    """Validate country code creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required fields
    country = data.get("country")
    if not country:
        errors["country"] = "Country is required."
    else:
        cleaned_data["country"] = country

    code = data.get("code")
    if not code:
        errors["code"] = "Country code is required."
    else:
        # Check uniqueness
        existing = PhoneCountryCode.objects.filter(
            code=code, 
            deleted=False
        )
        if existing.exists():
            errors["code"] = "Country code already exists."
        else:
            cleaned_data["code"] = code

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }

def validate_custom_field_payload(data):
    """Validate custom field creation/update payload"""
    errors = {}
    cleaned_data = {}

    # Required fields
    field_key = data.get("field_key")
    if not field_key:
        errors["field_key"] = "Field key is required."
    else:
        # Check uniqueness
        existing = EmployeeCustomFieldConfig.objects.filter(
            field_key=field_key, 
            deleted=False
        )
        if existing.exists():
            errors["field_key"] = "Field key already exists."
        else:
            cleaned_data["field_key"] = field_key

    field_label = data.get("field_label")
    if not field_label:
        errors["field_label"] = "Field label is required."
    else:
        cleaned_data["field_label"] = field_label

    # Field type FK
    field_type_id = data.get("field_type")
    if field_type_id:
        try:
            cleaned_data["field_type"] = FieldType.objects.get(id=field_type_id)
        except ObjectDoesNotExist:
            errors["field_type"] = f"FieldType with id {field_type_id} does not exist."

    # Optional boolean fields
    is_selected = data.get("is_selected", False)
    cleaned_data["is_selected"] = is_selected

    is_required = data.get("is_required", False)
    cleaned_data["is_required"] = is_required

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "cleaned_data": cleaned_data
    }