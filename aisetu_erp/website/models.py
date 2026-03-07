from django.db import models
import random
import string
    
class DemoRequest(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    store_type = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.contact_number}"


class UserLogin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class PricingSignup(models.Model):
    shop_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=15)
    referral_code = models.CharField(max_length=50, blank=True, null=True)
    total_referrals = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name

class PhonePeTransaction(models.Model):
    merchant_transaction_id = models.CharField(max_length=100, unique=True)
    phonepe_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField()  # Amount in paise
    status = models.CharField(max_length=50, default='PAYMENT_PENDING')
    user_phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.merchant_transaction_id} - {self.status}"

class LandingPageContent(models.Model):
    # Singleton model for Landing Page Content
    # Hero Section
    hero_eyebrow = models.CharField(max_length=200, default="India's Smartest Retail ERP")
    hero_title = models.CharField(max_length=200, default="Smart ERP for")
    hero_highlighted_title = models.CharField(max_length=200, default="Indian Retailers")
    hero_subtitle = models.TextField(default="AI-powered billing, inventory & store management — built specifically for Indian retail businesses. Save time, reduce errors, grow faster.")
    
    # Highlights (stored as comma-separated string for simplicity in admin)
    hero_highlights = models.CharField(max_length=500, default="GST-Ready Billing,Real-time Inventory,AI-Powered Insights")
    
    # CTA Buttons
    primary_cta_text = models.CharField(max_length=50, default="Book Free Demo")
    secondary_cta_text = models.CharField(max_length=50, default="Watch Demo")
    
    # Social Proof
    trusted_retailers_count = models.CharField(max_length=50, default="500+")
    
    # Floating Stats
    hero_stats_label = models.CharField(max_length=100, default="Today's Sales")
    hero_stats_value = models.CharField(max_length=50, default="₹1,24,500")

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if LandingPageContent.objects.exists() and not self.pk:
            # if an instance exists, maybe update it instead or reject creation
            # to be safe, just get the first and update
            existing = LandingPageContent.objects.first()
            self.pk = existing.pk
        super(LandingPageContent, self).save(*args, **kwargs)

    def __str__(self):
        return "Landing Page Content Settings"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    # countryCode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    officeAddress = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class JobApplication(models.Model):

    job_position = models.CharField(max_length=200)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    experience = models.IntegerField(null=True, blank=True)
    available_to_join = models.IntegerField(null=True, blank=True)

    current_salary = models.CharField(max_length=100, blank=True)
    expected_salary = models.CharField(max_length=100, blank=True)

    location = models.CharField(max_length=200)

    resume = models.FileField(upload_to="resumes/")

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.job_position}"

def generate_referral_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=6))


class ReferralUser(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    referral_code = models.CharField(max_length=6, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_referral_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.mobile_number