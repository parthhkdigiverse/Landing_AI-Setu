from django.db import models
import random
import string
import uuid
from django.utils.text import slugify
    
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

class AdminUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    
class PricingSignup(models.Model):
    shop_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=15, unique=True)

    referral_code = models.CharField(max_length=50, null=True)
    total_referrals = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name


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

    trust_item1 = models.CharField(max_length=200, default="Made for Indian Retailers")
    trust_item2 = models.CharField(max_length=200, default="GST-Ready")
    trust_item3 = models.CharField(max_length=200, default="Secure Cloud Data")
    trust_item4 = models.CharField(max_length=200, default="24/7 Support")

    problem_section_label = models.CharField(
        max_length=100,
        default="THE CHALLENGE"
    )

    problem_section_title = models.CharField(
        max_length=255,
        default="Retailers Face These Daily Problems"
    )

    feature_title = models.CharField(
        max_length=100,
        default="Features",
        
    )

    feature_title2 = models.CharField(
        max_length=100,
        default="Everything you need to run your retail business smarter.",
        
    )

    solution_section_label = models.CharField(
        max_length=100,
        default="THE SOLUTION",
        
    )

    solution_section_title = models.CharField(
        max_length=255,
        default="One Smart ERP For Complete Store Management",
        
    )


    usp_badge_text = models.CharField(
        max_length=200,
        default="AI-Powered (Beta Feature)",
        
    )

    usp_title = models.CharField(
        max_length=200,
        default="No Barcode? No Problem.",
        
    )

    usp_description = models.TextField(
        default="Our AI technology identifies products from photos — just snap and bill. No barcode scanner needed. Lightning-fast, accurate, and incredibly simple.",
        
    )

    # ===============================
    # HOW IT WORKS SECTION
    # ===============================

    howitworks_label = models.CharField(
        max_length=100,
        default="Simple Process",
        
    )

    howitworks_title = models.CharField(
        max_length=255,
        default="How It Works",
        
    )


    # ===============================
    # WHO IS THIS FOR
    # ===============================
    who_main_title = models.CharField(
        max_length=255,
        default="Perfect For",
        
    )

    who_title = models.CharField(
        max_length=255,
        default="Who Is This For?",
        
    )


    # ----------------------------
    # Pricing Section
    # ----------------------------

    pricing_main_title = models.CharField(max_length=255, default="Pricing")
    pricing_main_desc = models.CharField(max_length=255, default="Simple, transparent pricing — one package, everything included.")

    pricing_label = models.CharField(
        max_length=100,
        default="PRICING",
        
    )

    pricing_title = models.CharField(
        max_length=255,
        default="Simple & Transparent Pricing",
        
    )

    # Plan Title
    pricing_plan_name = models.CharField(
        max_length=200,
        default="All-Inclusive Package",
        
    )

    # Old Price
    pricing_old_price = models.CharField(
        max_length=50,
        default="₹29,999",
        
    )

    # Current Price
    pricing_price = models.CharField(
        max_length=50,
        default="₹12,000",
        
    )

    pricing_price_suffix = models.CharField(
        max_length=50,
        default="+ GST",
        
    )

    # ----------------------------
    # Features
    # ----------------------------

    pricing_feature1 = models.CharField(
        max_length=255,
        default="Full Access to All Modules",
        
    )

    pricing_feature2 = models.CharField(
        max_length=255,
        default="POS Billing + Inventory",
        
    )

    pricing_feature3 = models.CharField(
        max_length=255,
        default="CRM & Loyalty Programs",
        
    )

    pricing_feature4 = models.CharField(
        max_length=255,
        default="Accounting & Reports",
        
    )

    pricing_feature5 = models.CharField(
        max_length=255,
        default="Employee Management",
        
    )

    pricing_feature6 = models.CharField(
        max_length=255,
        default="Setup & Training Support",
        
    )

    pricing_feature7 = models.CharField(
        max_length=255,
        default="24/7 Customer Support",
        
    )

    pricing_feature8 = models.CharField(
        max_length=255,
        default="AI Photo Billing",
        
    )

    # ----------------------------
    # Referral Section
    # ----------------------------
    
    referral_main_title = models.CharField(
        max_length=255,
        default="Referral Program",
        
    )

    referral_main_desc = models.CharField(
        max_length=255,
        default="Earn money by referring retailers to AI-Setu ERP.",
        
    )


    referral_label = models.CharField(
        max_length=100,
        default="REFERRAL PROGRAM",
        
    )

    referral_title = models.CharField(
        max_length=255,
        default="Earn With AI-Setu ERP",
        
    )


    join_referral = models.CharField(max_length=50, default="Join Referral Program")

    # ----------------------------
    # Comparison Section
    # ----------------------------

    comparison_title = models.CharField(
        max_length=255,
        default="AI-Setu ERP vs Traditional Software",
        
    )

    comparison_subtitle = models.CharField(
        max_length=255,
        default="Discover why retailers are switching to AI-Setu ERP for faster, smarter store management.",
        
    )
    comparison_title1 = models.CharField(max_length=200, default="Feature")
    comparison_title2 = models.CharField(max_length=200, default="AI-Setu ERP")
    comparison_title3 = models.CharField(max_length=200, default="Traditional")

    # ----------------------------
    # Testimonials Section
    # ----------------------------

    testimonial_label = models.CharField(
        max_length=100,
        default="TESTIMONIALS",
        
    )

    testimonial_title = models.CharField(
        max_length=255,
        default="What Our Customers Say",
        
    )

    review_button = models.CharField(max_length=50, default="View All Reviews")

    all_reviews_title = models.CharField(
        max_length=255,default="Customer Reviews")
    
    all_reviews_desc = models.CharField(
        max_length=255,default="See what retailers across India are saying about AI-Setu ERP.")

    # ----------------------------
    # FAQ Section
    # ----------------------------

    faq_title = models.CharField(
        max_length=255,
        default="Frequently Asked Questions",
        
    )


    # CTA SECTION

    cta_badge = models.CharField(
        max_length=200,
        default="Join 500+ Happy Retailers",
        
    )

    cta_title = models.CharField(
        max_length=255,
        default="Ready to Upgrade Your Store?",
        
    )

    cta_description = models.TextField(
        default="Join hundreds of Indian retailers who've switched to smarter billing with AI-Setu ERP. Get started in minutes, no tech skills needed.",
        
    )

    cta_button_text = models.CharField(
        max_length=100,
        default="Book Free Demo",
        
    )

    cta_small_text = models.CharField(
        max_length=255,
        default="No credit card required · Free setup · Cancel anytime",
        
    )

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


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts")
    
    featured_image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    excerpt = models.TextField(help_text="A short summary of the post.")
    content = models.TextField()
    
    author = models.CharField(max_length=100, default="Admin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class JobApplication(models.Model):

    job_position = models.CharField(max_length=200)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    experience = models.IntegerField(null=True, )
    available_to_join = models.IntegerField(null=True, )

    current_salary = models.CharField(max_length=100, )
    expected_salary = models.CharField(max_length=100, )

    location = models.CharField(max_length=200)

    resume = models.FileField(upload_to="resumes/")

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.job_position}"

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class ReferralUser(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    referral_code = models.CharField(max_length=10, default=generate_referral_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile_number

class Payment(models.Model):

    pricing_signup = models.ForeignKey(PricingSignup, on_delete=models.CASCADE)

    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)

    amount = models.IntegerField()

    status = models.CharField(max_length=20, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)

    invoice = models.FileField(upload_to="invoices/", null=True, )

    def __str__(self):
        return str(self.transaction_id)

from django.db import models


# class AboutPageContent(models.Model):

#     # ==========================
#     # HERO SECTION
#     # ==========================

#     hero_title = models.CharField(
#         max_length=255,
#         default="About AI-Setu ERP",
#         blank=True
#     )

#     hero_description = models.TextField(
#         default="AI-Setu ERP empowers retailers with modern technology to simplify store management. We help SMEs automate operations, improve efficiency, and grow faster with intelligent ERP solutions.",
#         blank=True
#     )


#     # ==========================
#     # ABOUT CONTENT SECTION
#     # ==========================

#     about_label = models.CharField(
#         max_length=100,
#         default="ABOUT US",
#         blank=True
#     )

#     about_heading = models.CharField(
#         max_length=255,
#         default="WE ARE ON A DRIVE TO MAKE THE RETAIL INDUSTRY MORE EFFICIENT.",
#         blank=True
#     )

#     about_description_1 = models.TextField(
#         default="AI-Setu ERP is the future of retail. From empowering offline stores to managing their inventory and sales with smart technology.",
#         blank=True
#     )

#     about_description_2 = models.TextField(
#         default="SMEs often struggle to find a comprehensive cloud-based ERP and POS solution that can scale with their growth.",
#         blank=True
#     )

#     about_description_3 = models.TextField(
#         default="AI-Setu ERP empowers SMEs to use modern ERP tools without complexity and grow their business with automation and analytics.",
#         blank=True
#     )

#     # ==========================
#     # MISSION SECTION
#     # ==========================

#     mission_title = models.CharField(
#         max_length=200,
#         default="Our Mission",
#         blank=True
#     )

#     mission_description = models.TextField(
#         default="Retail businesses are the backbone of the Indian economy, yet many rely on outdated tools. AI-Setu ERP brings modern technology to retail businesses, enabling inventory tracking, billing, sales analytics, and smarter decisions with ease.",
#         blank=True
#     )


#     # ==========================
#     # WHY CHOOSE US SECTION
#     # ==========================

#     why_choose_title = models.CharField(
#         max_length=200,
#         default="Why Choose AI-Setu ERP?",
#         blank=True
#     )

#     why_point_1 = models.CharField(
#         max_length=200,
#         default="Smart AI-powered billing",
#         blank=True
#     )

#     why_point_2 = models.CharField(
#         max_length=200,
#         default="Fast and reliable billing",
#         blank=True
#     )

#     why_point_3 = models.CharField(
#         max_length=200,
#         default="Real-time inventory tracking",
#         blank=True
#     )

#     why_point_4 = models.CharField(
#         max_length=200,
#         default="Powerful sales analytics",
#         blank=True
#     )

#     why_point_5 = models.CharField(
#         max_length=200,
#         default="Built specifically for Indian retailers",
#         blank=True
#     )


#     # ==========================
#     # WHO DO WE SERVE SECTION
#     # ==========================

#     serve_title = models.CharField(
#         max_length=200,
#         default="WHO DO WE SERVE?",
#         blank=True
#     )

#     serve_subtitle = models.CharField(
#         max_length=255,
#         default="We serve all types of retail businesses with our ERP solutions.",
#         blank=True
#     )


#     # Retail Category 1
#     serve1_title = models.CharField(
#         max_length=200,
#         default="Kirana Store",
#         blank=True
#     )

#     # Retail Category 2
#     serve2_title = models.CharField(
#         max_length=200,
#         default="General Store",
#         blank=True
#     )

#     # Retail Category 3
#     serve3_title = models.CharField(
#         max_length=200,
#         default="Medical Store",
#         blank=True
#     )

#     # Retail Category 4
#     serve4_title = models.CharField(
#         max_length=200,
#         default="Hardware Store",
#         blank=True
#     )


#     # ==========================
#     # BOTTOM CTA SECTION
#     # ==========================

#     cta_title = models.CharField(
#         max_length=255,
#         default="Transform Your Retail Business",
#         blank=True
#     )

#     cta_description = models.TextField(
#         default="Join retailers who are already using AI-Setu ERP to streamline operations.",
#         blank=True
#     )

#     cta_button_text = models.CharField(
#         max_length=100,
#         default="Book Free Demo",
#         blank=True
#     )

#     updated_at = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return "About Page Content"
    

class ContactPageContent(models.Model):

    # HERO SECTION
    hero_title = models.CharField(
        max_length=200,
        default="Let's Start a Conversation"
    )

    hero_description = models.TextField(
        default="Ready to transform your business with AI? We're here to help you every step of the way. Reach out and let's build something amazing together."
    )

    # CONTACT CARDS SECTION

    # Call Us
    call_title = models.CharField(
        max_length=100,
        default="Call Us"
    )

    call_phone = models.CharField(
        max_length=20,
        default="+91 98765 43210"
    )

    call_phone_number = models.CharField(
        max_length=20,
        default="+919876543210",
        blank=True
    )

    call_subtext = models.CharField(
        max_length=100,
        default="Mon–Sat 9:30AM to 6:30PM"
    )

    # Email Us
    email_title = models.CharField(
        max_length=100,
        default="Email Us"
    )

    email_address = models.EmailField(
        default="hello@aisetuerp.com"
    )

    email_address_link = models.EmailField(
        default="hello@aisetuerp.com",
        blank=True
    )

    email_subtext = models.CharField(
        max_length=100,
        default="We'll respond within 24 hours"
    )

    # Visit Us
    visit_title = models.CharField(
        max_length=100,
        default="Visit Us"
    )

    visit_address = models.CharField(
        max_length=255,
        default="Surat, India"
    )

    visit_subtext = models.CharField(
        max_length=100,
        default="Schedule a meeting"
    )

    visit_map_url = models.URLField(
        default="https://goo.gl/maps/example",
        blank=True
    )

    # Support Hours
    support_title = models.CharField(
        max_length=100,
        default="Support Hours"
    )

    support_time = models.CharField(
        max_length=100,
        default="24/7 Available"
    )

    support_subtext = models.CharField(
        max_length=100,
        default="Always here to help"
    )

    # CONTACT FORM SECTION

    form_title = models.CharField(
        max_length=200,
        default="Send us a Message"
    )

    name_label = models.CharField(
        max_length=100,
        default="Full Name"
    )

    name_placeholder = models.CharField(
        max_length=200,
        default="Enter your full name"
    )


    phone_label = models.CharField(
        max_length=100,
        default="Phone Number"
    )

    phone_placeholder = models.CharField(
        max_length=200,
        default="Enter your phone number"
    )


    email_label = models.CharField(
        max_length=100,
        default="Email Address"
    )

    email_placeholder = models.CharField(
        max_length=200,
        default="Enter your email address"
    )


    company_label = models.CharField(
        max_length=100,
        default="Office Address"
    )

    company_placeholder = models.CharField(
        max_length=200,
        default="Enter your office address"
    )


    message_label = models.CharField(
        max_length=100,
        default="Message"
    )

    message_placeholder = models.CharField(
        max_length=200,
        default="Tell us about your requirements..."
    )


    form_button_text = models.CharField(
        max_length=100,
        default="Send Message"
    )

    # WHY CHOOSE SECTION

    why_title = models.CharField(
        max_length=200,
        default="Why Choose AI-Setu?"
    )

    why_description = models.TextField(
        default="We're not just another ERP solution. We're your technology partner, committed to transforming your business operations with cutting-edge AI and personalized support."
    )

    feature_1_title = models.CharField(
        max_length=100,
        default="Experienced Team"
    )

    feature_2_title = models.CharField(
        max_length=100,
        default="Fast Implementation"
    )

    feature_3_title = models.CharField(
        max_length=100,
        default="24/7 Support"
    )

    feature_4_title = models.CharField(
        max_length=100,
        default="Quick Response"
    )

    # CTA SECTION

    cta_title = models.CharField(
        max_length=200,
        default="Ready to Get Started?"
    )

    cta_description = models.TextField(
        default="Join hundreds of businesses already using AI-Setu to streamline their operations and boost productivity."
    )

    cta_button_text1 = models.CharField(
        max_length=100,
        default="Free Consultation"
    )

    cta_button_text2 = models.CharField(
        max_length=100,
        default="Custom Solutions"
    )

    cta_button_text3 = models.CharField(
        max_length=100,
        default="24/7 Support"
    )

    def __str__(self):
        return "Contact Page Content"
    
class Problem(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    icon = models.CharField(
        max_length=50,
        help_text="lucide-react icon name (clock, package, trending-down, users, barcode)"
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Challanges"
        ordering = ["order"]

class Feature(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    icon = models.CharField(
        max_length=50,
        help_text="lucide-react icon name (zap, bar-chart, shield, etc)"
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]

class USPFeature(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    icon = models.CharField(max_length=50)

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]

class HowItWorksStep(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    icon = models.CharField(max_length=50)

    step_number = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Step {self.step_number} - {self.title}"

    class Meta:
        ordering = ["step_number"]

class StoreType(models.Model):

    title = models.CharField(max_length=200)

    icon = models.CharField(max_length=50)

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Who Is This For - Store Types"
        ordering = ["order"]

class ReferralPerk(models.Model):

    value = models.CharField(max_length=100)
    text = models.CharField(max_length=255)

    icon = models.CharField(max_length=50)

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Referral Perk"

    class Meta:
        ordering = ["order"]

class Testimonial(models.Model):

    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    review = models.TextField()

    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)

    rating = models.IntegerField(default=5)

    is_active = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

class ComparisonFeature(models.Model):
    feature_name = models.CharField(max_length=255)
    has_ai_setu = models.BooleanField(default=True)
    has_traditional = models.BooleanField(default=False)
    order = models.IntegerField(default=0)  # display sequence
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.feature_name

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question
    
class LoginLink(models.Model):
    label = models.CharField(max_length=100, default="Login")
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.label

class DemoVideo(models.Model):

    title = models.CharField(max_length=200, default="Watch Demo")

    video_url = models.URLField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AllStoreType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Store Type"
        verbose_name_plural = "Demo Form Store Types"

class Footer(models.Model):

    # Logo description
    description = models.TextField(
        default="Smart ERP for Indian retailers. AI-powered billing & store management."
    )

    # Contact
    email = models.EmailField(default="ceo@hkdigiverse.com")
    address = models.TextField(default="501-502, Silver Trade Center, Mota Varachha, Surat, Gujarat, India - 394101")
    phone = models.CharField(max_length=20, default="+91 12345 67890")

    # Links
    quick_links = models.JSONField(default=list)
    policies = models.JSONField(default=list)

    def __str__(self):
        return "Footer Content"
    
from django.db import models


class CareerPage(models.Model):
    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.TextField()

    culture_title = models.CharField(max_length=200, default="Our Culture")
    perks_title = models.CharField(max_length=200, default="Perks & Benefits")

    cta_title = models.CharField(max_length=255)
    cta_subtitle = models.TextField()
    cta_button_text = models.CharField(max_length=100)

    def __str__(self):
        return "Career Page"


class Culture(models.Model):
    career_page = models.ForeignKey(
        CareerPage,
        on_delete=models.CASCADE,
        related_name="cultures"
    )
    icon = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Perk(models.Model):
    career_page = models.ForeignKey(
        CareerPage,
        on_delete=models.CASCADE,
        related_name="perks"
    )
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class JobPosition(models.Model):
    career_page = models.ForeignKey(
        CareerPage,
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    title = models.CharField(max_length=200)
    job_slug = models.SlugField(unique=True, blank=True, null=True)
    experience = models.CharField(max_length=100)
    total_positions = models.IntegerField(default=1)
    work_place = models.CharField(max_length=100, default="WFO")
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class ChildJobPosition(models.Model):
    career_page = models.ForeignKey(
        CareerPage,
        on_delete=models.CASCADE,
        related_name="job"
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    location = models.CharField(max_length=200)
    experience = models.CharField(max_length=100)
    

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class JobDescription(models.Model):
    job = models.ForeignKey(
        ChildJobPosition,
        on_delete=models.CASCADE,
        related_name="descriptions"
    )

    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class JobSkill(models.Model):
    job = models.ForeignKey(
        ChildJobPosition,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


# SECTION (Hero, About, Mission, etc.)
class Section(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=100)  # e.g. hero, about, mission
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='sections/', blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.page.title} - {self.name}"


# ITEMS inside section (cards, bullet points, etc.)
class SectionItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='section_items/', blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title or "Item"

class Policy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True)  # ✅ Intro text

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Policy.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PolicySection(models.Model):
    policy = models.ForeignKey(
        Policy, related_name="sections", on_delete=models.CASCADE
    )
    heading = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.policy.title} - {self.heading}"