from django.db import models

class Onboarding(models.Model):
    # 1. Basic Details
    employee_name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    work_location = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    mobile_number = models.CharField(max_length=20)
    email_id = models.EmailField()

    # 2. Personal Details
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tshirt_size = models.CharField(max_length=10, blank=True, null=True)

    # 3. Emergency Contact
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_relationship = models.CharField(max_length=100, blank=True, null=True)
    emergency_number = models.CharField(max_length=20, blank=True, null=True)

    # 4. Bank Details
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=50, blank=True, null=True)
    bank_branch = models.CharField(max_length=100, blank=True, null=True)
    # Placeholder for attachment path
    cancelled_cheque = models.FileField(upload_to='bank_proofs/', blank=True, null=True)

    # 5. ID Card Details
    photo_submitted = models.CharField(max_length=10, blank=True, null=True)
    id_card_blood_group = models.CharField(max_length=20, blank=True, null=True)

    # 6. Documents Submitted (Store as Boolean)
    doc_aadhaar = models.BooleanField(default=False)
    doc_pan = models.BooleanField(default=False)
    doc_bank_proof = models.BooleanField(default=False)
    doc_passport_photo = models.BooleanField(default=False)
    doc_education_cert = models.BooleanField(default=False)
    doc_resume = models.BooleanField(default=False)
    doc_driving_license = models.BooleanField(default=False)

    # 7. Additional Info
    total_experience = models.CharField(max_length=100, blank=True, null=True)
    hp_experience = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=50, blank=True, null=True)

    # Timestamps and internal tracking
    status = models.CharField(max_length=20, default='Completed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} ({self.status})"
