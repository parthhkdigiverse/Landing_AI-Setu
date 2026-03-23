import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
django.setup()

from website.models import LandingPageContent, HowItWorksStep

try:
    all_content = LandingPageContent.objects.all()
    print(f"Total LandingPageContent objects: {all_content.count()}")
    for c in all_content:
        steps_count = HowItWorksStep.objects.filter(landing_page=c).count()
        print(f"Content ID: {c.id}, Steps linked: {steps_count}")
        
except Exception as e:
    print("ERROR:", e)
