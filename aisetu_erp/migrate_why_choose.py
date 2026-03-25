import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
django.setup()

from website.models import AboutPageContent, AboutUsWhyChooseItem

def migrate():
    content = AboutPageContent.objects.first()
    if not content:
        print("No AboutPageContent found.")
        return

    points = [
        content.why_point_1,
        content.why_point_2,
        content.why_point_3,
        content.why_point_4,
        content.why_point_5
    ]

    created_count = 0
    for i, point in enumerate(points):
        if point:
            # Check if this point already exists in dynamic (simple title check)
            if not AboutUsWhyChooseItem.objects.filter(about_page=content, title=point).exists():
                AboutUsWhyChooseItem.objects.create(
                    about_page=content,
                    title=point,
                    order=i,
                    is_active=True
                )
                print(f"Migrated point: {point}")
                created_count += 1
            else:
                print(f"Point already exists, skipping: {point}")
    
    print(f"Migration complete. {created_count} points migrated.")

if __name__ == "__main__":
    migrate()
