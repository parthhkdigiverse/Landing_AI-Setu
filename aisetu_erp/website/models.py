from django.db import models
import random
import string
import uuid
    
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

    # Problem Card 1
    problem1_title = models.CharField(max_length=200, default="Slow Billing")
    problem1_description = models.TextField(default="Manual billing wastes time & creates long queues")

    # Problem Card 2
    problem2_title = models.CharField(max_length=200, default="No Stock Control")
    problem2_description = models.TextField(default="Inventory mismatches lead to lost sales")

    # Problem Card 3
    problem3_title = models.CharField(max_length=200, default="Unknown Profit Margin")
    problem3_description = models.TextField(default="Can't track real profit per product")

    # Problem Card 4
    problem4_title = models.CharField(max_length=200, default="Staff Dependency")
    problem4_description = models.TextField(default="Business stops when key staff is absent")

    # Problem Card 5
    problem5_title = models.CharField(max_length=200, default="Barcode Not Available")
    problem5_description = models.TextField(default="Most Indian products lack barcodes")

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

    # Card 1
    solution1_title = models.CharField(
        max_length=200,
        default="POS Billing",
        
    )

    solution1_desc = models.TextField(
        default="Lightning-fast billing with GST compliance",
        
    )

    # Card 2
    solution2_title = models.CharField(
        max_length=200,
        default="Inventory Management",
        
    )

    solution2_desc = models.TextField(
        default="Real-time stock tracking & alerts",
        
    )

    # Card 3
    solution3_title = models.CharField(
        max_length=200,
        default="CRM & Loyalty",
        
    )

    solution3_desc = models.TextField(
        default="Customer management & loyalty programs",
        
    )

    # Card 4
    solution4_title = models.CharField(
        max_length=200,
        default="Accounting",
        
    )

    solution4_desc = models.TextField(
        default="Automated bookkeeping & reports",
        
    )

    # Card 5
    solution5_title = models.CharField(
        max_length=200,
        default="Employee Management",
        
    )

    solution5_desc = models.TextField(
        default="Attendance, payroll & performance",
        
    )

    # Card 6
    solution6_title = models.CharField(
        max_length=200,
        default="Reports & Dashboard",
        
    )

    solution6_desc = models.TextField(
        default="Insights at a glance with smart analytics",
        
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

    # Feature 1
    usp_feature1_title = models.CharField(max_length=200, default="Photo-Based Product Detection")
    usp_feature1_desc = models.TextField(default="Instant product recognition from images")

    # Feature 2
    usp_feature2_title = models.CharField(max_length=200, default="AI Auto Identify Product")
    usp_feature2_desc = models.TextField(default="Smart AI-powered identification system")

    # Feature 3
    usp_feature3_title = models.CharField(max_length=200, default="Add Directly to Bill")
    usp_feature3_desc = models.TextField(default="Seamless one-click billing integration")

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

    howitworks_step1_title = models.CharField(
        max_length=200,
        default="Book Demo",
        
    )

    howitworks_step1_desc = models.CharField(
        max_length=255,
        default="Schedule a quick demo with our team",
        
    )

    howitworks_step2_title = models.CharField(
        max_length=200,
        default="Setup & Training",
        
    )

    howitworks_step2_desc = models.CharField(
        max_length=255,
        default="We configure everything for you",
        
    )

    howitworks_step3_title = models.CharField(
        max_length=200,
        default="Start Smart Billing",
        
    )

    howitworks_step3_desc = models.CharField(
        max_length=255,
        default="Go live and start selling instantly",
        
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

    who1 = models.CharField(
        max_length=200,
        default="Kirana Stores",
        
    )

    who2 = models.CharField(
        max_length=200,
        default="General Stores",
        
    )

    who3 = models.CharField(
        max_length=200,
        default="Medical Shops",
        
    )

    who4 = models.CharField(
        max_length=200,
        default="Hardware Stores",
        
    )

    who5 = models.CharField(
        max_length=200,
        default="Margin Business Retailers",
        
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

    referral_item1_value = models.CharField(
        max_length=100,
        default="₹2,000",
        
    )

    referral_item1_text = models.CharField(
        max_length=200,
        default="Per Successful Sale",
        
    )

    referral_item2_value = models.CharField(
        max_length=100,
        default="₹1,000",
        
    )

    referral_item2_text = models.CharField(
        max_length=200,
        default="Renewal Incentive",
        
    )

    referral_item3_value = models.CharField(
        max_length=100,
        default="₹1,000",
        
    )

    referral_item3_text = models.CharField(
        max_length=200,
        default="For Every Successful Referral Purchase",
        
    )

    referral_item4_value = models.CharField(
        max_length=100,
        default="Unlimited",
        
    )

    referral_item4_text = models.CharField(
        max_length=200,
        default="Referral Income",
        
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

    comparison_feature1 = models.CharField(max_length=200, default="AI Photo Billing")
    comparison_feature2 = models.CharField(max_length=200, default="Simple Interface")
    comparison_feature3 = models.CharField(max_length=200, default="One Package Pricing")
    comparison_feature4 = models.CharField(max_length=200, default="Retail-Focused")
    comparison_feature5 = models.CharField(max_length=200, default="GST Ready")
    comparison_feature6 = models.CharField(max_length=200, default="Cloud Access")
    comparison_feature7 = models.CharField(max_length=200, default="24/7 Support")


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

    testimonial1_name = models.CharField(
        max_length=200,
        default="Rajesh Patel",
        
    )

    testimonial1_role = models.CharField(
        max_length=200,
        default="Kirana Store,Surat",
        
    )

    testimonial1_text = models.TextField(
        default="AI-Setu ERP transformed my billing process. The AI photo detection is a game changer — no more barcode hassles!",
        
    )

    testimonial2_name = models.CharField(
        max_length=200,
        default="Priya Sharma",
        
    )

    testimonial2_role = models.CharField(
        max_length=200,
        default="Medical Shop,Surat",
        
    )

    testimonial2_text = models.TextField(
        default="Simple to use and my staff learned it in one day. GST billing is now automatic. Highly recommended!",
        
    )

    testimonial3_name = models.CharField(
        max_length=200,
        default="Amit Desai",
        
    )

    testimonial3_role = models.CharField(
        max_length=200,
        default="General Store, Vadodara",
        
    )

    testimonial3_text = models.TextField(
        default="Finally an ERP that understands Indian retail. The pricing is fair and support team is always available.",
        
    )

    # ----------------------------
    # FAQ Section
    # ----------------------------

    faq_title = models.CharField(
        max_length=255,
        default="Frequently Asked Questions",
        
    )

    faq1_question = models.CharField(
        max_length=255,
        default="Is it GST Ready?",
        
    )

    faq1_answer = models.TextField(
        default="Yes! AI-Setu ERP is fully GST compliant with automatic tax calculations, GSTIN integration, and GST-ready invoicing.",
        
    )

    faq2_question = models.CharField(
        max_length=255,
        default="Is Internet Required?",
        
    )

    faq2_answer = models.TextField(
        default="AI-Setu ERP is cloud-based for the best experience. However, basic billing can work offline and syncs when internet is available.",
        
    )

    faq3_question = models.CharField(
        max_length=255,
        default="Do I need Barcode?",
        
    )

    faq3_answer = models.TextField(
        default="No! Our AI-powered photo detection lets you bill products without barcodes — just snap a photo and the product is identified automatically.",
        
    )

    faq4_question = models.CharField(
        max_length=255,
        default="Is Support Provided?",
        
    )

    faq4_answer = models.TextField(
        default="Yes, we provide 24/7 customer support via phone, email, and chat. Our team is always ready to help.",
        
    )

    faq5_question = models.CharField(
        max_length=255,
        default="Is Training Included?",
        
    )

    faq5_answer = models.TextField(
        default="Absolutely. We provide complete setup and training for you and your staff as part of the package.",
        
    )

    faq6_question = models.CharField(
        max_length=255,
        default="What About Renewal?",
        
    )

    faq6_answer = models.TextField(
        default="Annual renewal is available at a competitive rate. Refer others and earn ₹1,000 per renewal incentive!",
        
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


class AboutPageContent(models.Model):

    # ==========================
    # HERO SECTION
    # ==========================

    hero_title = models.CharField(
        max_length=255,
        default="About AI-Setu ERP",
        blank=True
    )

    hero_description = models.TextField(
        default="AI-Setu ERP empowers retailers with modern technology to simplify store management. We help SMEs automate operations, improve efficiency, and grow faster with intelligent ERP solutions.",
        blank=True
    )


    # ==========================
    # ABOUT CONTENT SECTION
    # ==========================

    about_label = models.CharField(
        max_length=100,
        default="ABOUT US",
        blank=True
    )

    about_heading = models.CharField(
        max_length=255,
        default="WE ARE ON A DRIVE TO MAKE THE RETAIL INDUSTRY MORE EFFICIENT.",
        blank=True
    )

    about_description_1 = models.TextField(
        default="AI-Setu ERP is the future of retail. From empowering offline stores to managing their inventory and sales with smart technology.",
        blank=True
    )

    about_description_2 = models.TextField(
        default="SMEs often struggle to find a comprehensive cloud-based ERP and POS solution that can scale with their growth.",
        blank=True
    )

    about_description_3 = models.TextField(
        default="AI-Setu ERP empowers SMEs to use modern ERP tools without complexity and grow their business with automation and analytics.",
        blank=True
    )

    # ==========================
    # MISSION SECTION
    # ==========================

    mission_title = models.CharField(
        max_length=200,
        default="Our Mission",
        blank=True
    )

    mission_description = models.TextField(
        default="Retail businesses are the backbone of the Indian economy, yet many rely on outdated tools. AI-Setu ERP brings modern technology to retail businesses, enabling inventory tracking, billing, sales analytics, and smarter decisions with ease.",
        blank=True
    )


    # ==========================
    # WHY CHOOSE US SECTION
    # ==========================

    why_choose_title = models.CharField(
        max_length=200,
        default="Why Choose AI-Setu ERP?",
        blank=True
    )

    why_point_1 = models.CharField(
        max_length=200,
        default="Smart AI-powered billing",
        blank=True
    )

    why_point_2 = models.CharField(
        max_length=200,
        default="Fast and reliable billing",
        blank=True
    )

    why_point_3 = models.CharField(
        max_length=200,
        default="Real-time inventory tracking",
        blank=True
    )

    why_point_4 = models.CharField(
        max_length=200,
        default="Powerful sales analytics",
        blank=True
    )

    why_point_5 = models.CharField(
        max_length=200,
        default="Built specifically for Indian retailers",
        blank=True
    )


    # ==========================
    # WHO DO WE SERVE SECTION
    # ==========================

    serve_title = models.CharField(
        max_length=200,
        default="WHO DO WE SERVE?",
        blank=True
    )

    serve_subtitle = models.CharField(
        max_length=255,
        default="We serve all types of retail businesses with our ERP solutions.",
        blank=True
    )


    # Retail Category 1
    serve1_title = models.CharField(
        max_length=200,
        default="Kirana Store",
        blank=True
    )

    # Retail Category 2
    serve2_title = models.CharField(
        max_length=200,
        default="General Store",
        blank=True
    )

    # Retail Category 3
    serve3_title = models.CharField(
        max_length=200,
        default="Medical Store",
        blank=True
    )

    # Retail Category 4
    serve4_title = models.CharField(
        max_length=200,
        default="Hardware Store",
        blank=True
    )


    # ==========================
    # BOTTOM CTA SECTION
    # ==========================

    cta_title = models.CharField(
        max_length=255,
        default="Transform Your Retail Business",
        blank=True
    )

    cta_description = models.TextField(
        default="Join retailers who are already using AI-Setu ERP to streamline operations.",
        blank=True
    )

    cta_button_text = models.CharField(
        max_length=100,
        default="Book Free Demo",
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "About Page Content"
    
from django.db import models

class CareerPageContent(models.Model):
    # ==========================
    # HERO SECTION
    # ==========================
    hero_title = models.CharField(
        max_length=255, 
        default="Build Your Career With AI-Setu 🚀"
    )
    hero_description = models.TextField(
        default="Join a team building the future of AI-powered ERP systems. Work with innovative people and solve real business problems."
    )

    # ==========================
    # OUR CULTURE SECTION
    # ==========================
    culture_title = models.CharField(max_length=200, default="Our Culture")
    
    # Culture Card 1
    culture_1_title = models.CharField(max_length=100, default="Collaboration")
    culture_1_desc = models.TextField(default="We believe teamwork builds better solutions.")
    
    # Culture Card 2
    culture_2_title = models.CharField(max_length=100, default="Innovation")
    culture_2_desc = models.TextField(default="Experiment and create new possibilities.")
    
    # Culture Card 3
    culture_3_title = models.CharField(max_length=100, default="Growth")
    culture_3_desc = models.TextField(default="Continuous learning and career growth.")
    
    # Culture Card 4
    culture_4_title = models.CharField(max_length=100, default="Trust")
    culture_4_desc = models.TextField(default="Transparency and respect always.")

    # ==========================
    # PERKS & BENEFITS SECTION
    # ==========================
    benefits_title = models.CharField(max_length=200, default="Perks & Benefits")
    benefit_1 = models.CharField(max_length=100, default="Flexible Work Culture")
    benefit_2 = models.CharField(max_length=100, default="5 Day Work Week")
    benefit_3 = models.CharField(max_length=100, default="Learning Budget")
    benefit_4 = models.CharField(max_length=100, default="Team Events")
    benefit_5 = models.CharField(max_length=100, default="Fast Career Growth")
    benefit_6 = models.CharField(max_length=100, default="Friendly Work Environment")

    # ==========================
    # OPEN POSITIONS SECTION
    # ==========================
    positions_title = models.CharField(max_length=200, default="Open Positions")
    
    # Job 1
    job_1_role = models.CharField(max_length=200, default="Frontend Developer")
    job_1_details = models.CharField(max_length=200, default="1-3 Years • Ahmedabad")
    
    # Job 2
    job_2_role = models.CharField(max_length=200, default="Backend Developer (Python/Django)")
    job_2_details = models.CharField(max_length=200, default="2-4 Years • Ahmedabad")
    
    # Job 3
    job_3_role = models.CharField(max_length=200, default="AI Engineer")
    job_3_details = models.CharField(max_length=200, default="2+ Years • Remote / Ahmedabad")

    # ==========================
    # BOTTOM CTA SECTION
    # ==========================
    cta_title = models.CharField(max_length=255, default="Ready to Join AI-Setu?")
    cta_description = models.TextField(default="Explore our current openings and apply today.")
    cta_button_text = models.CharField(max_length=100, default="View Openings")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Career Page Content"


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
    