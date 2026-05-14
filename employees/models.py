from django.db import models

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='employee_profile',    null=True,
    blank=True)
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('onleave', 'On Leave'),
    )
    BRANCH_CHOICES = (
        ('Chennai', 'Chennai'),
        ('Vellore', 'Vellore'),
        ('Salem', 'Salem'),
        ('Kanchipuram', 'Kanchipuram'),
        ('Hosur', 'Hosur')
    )
    employee_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, choices=BRANCH_CHOICES, default='Chennai')
    email = models.EmailField(unique=True, max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Detailed Earnings Breakdown
    basic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conveyance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    child_edu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    personal_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    incentive = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Detailed Deductions Breakdown
    epf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    esi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prof_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lwf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    staff_advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction_insurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Benefits Group (CTC Components)
    employer_epf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employer_esi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employer_insurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    petrol_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    work_lat = models.FloatField(null=True, blank=True, help_text="Allowed work location latitude")
    work_lon = models.FloatField(null=True, blank=True, help_text="Allowed work location longitude")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.employee_name