import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
django.setup()

from website.models import LandingPageContent, HowItWorksStep

try:
    content = LandingPageContent.objects.first()
    if content:
        print(f"LandingPageContent found: {content.id}")
        linked_steps = HowItWorksStep.objects.filter(landing_page=content)
        print(f"Steps linked to this content: {linked_steps.count()}")
        for s in linked_steps:
            print(f"  - {s.title} (active: {s.is_active})")
        
        orphan_steps = HowItWorksStep.objects.filter(landing_page__isnull=True)
        print(f"Orphan steps (no landing_page): {orphan_steps.count()}")
        for s in orphan_steps:
            print(f"  - {s.title}")
            
        all_steps = HowItWorksStep.objects.all()
        print(f"Total steps in DB: {all_steps.count()}")
    else:
        print("No LandingPageContent found!")
except Exception as e:
    print("ERROR:", e)
