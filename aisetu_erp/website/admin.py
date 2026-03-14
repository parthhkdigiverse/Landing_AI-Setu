from django.contrib import admin
from .models import AboutPageContent, CareerPageContent, ContactPageContent, ContactPageContent, Feature, HowItWorksStep, LandingPageContent, Problem, ReferralPerk, StoreType, Testimonial, USPFeature, BlogCategory, BlogPost

# ... existing code ...

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "created_at", "is_published"]
    list_filter = ["is_published", "category", "author"]
    search_fields = ["title", "content", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"

# @admin.register(LandingPageContent)
# class LandingPageContentAdmin(admin.ModelAdmin):
#     # To restrict adding more than one instance
#     def has_add_permission(self, request):
#         if self.model.objects.exists():
#             return False
#         return super().has_add_permission(request)

@admin.register(LandingPageContent)
class LandingPageContentAdmin(admin.ModelAdmin):

    change_form_template = "admin/live_preview_change_form.html"

@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):

    change_form_template = "admin/live_preview_aboutus_form.html"

@admin.register(CareerPageContent)
class CareerPageContentAdmin(admin.ModelAdmin):
    change_form_template = "admin/live_preview_career_form.html"

    # This ensures you always edit the same object
    def has_add_permission(self, request):
        if CareerPageContent.objects.exists():
            return False
        return True
    
@admin.register(ContactPageContent)
class ContactPageContentAdmin(admin.ModelAdmin):
    change_form_template = "admin/live_preview_contactus_form.html"

    # This ensures you always edit the same object
    def has_add_permission(self, request):
        if ContactPageContent.objects.exists():
            return False
        return True

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):

    list_display = ["title", "order", "is_active"]

    list_editable = ["order", "is_active"]

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):

    list_display = ["title", "order", "is_active"]

    list_editable = ["order", "is_active"]

@admin.register(USPFeature)
class USPFeatureAdmin(admin.ModelAdmin):

    list_display = ["title", "order", "is_active"]

    list_editable = ["order", "is_active"]

@admin.register(HowItWorksStep)
class HowItWorksStepAdmin(admin.ModelAdmin):

    list_display = ["step_number", "title", "is_active"]

    list_editable = ["is_active"]

@admin.register(StoreType)
class StoreTypeAdmin(admin.ModelAdmin):

    list_display = ["title", "order", "is_active"]

    list_editable = ["order", "is_active"]

@admin.register(ReferralPerk)
class ReferralPerkAdmin(admin.ModelAdmin):

    list_display = ["value", "text", "order", "is_active"]

    list_editable = ["order", "is_active"]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):

    list_display = ["name", "role", "rating", "is_active", "order"]

    list_editable = ["rating", "is_active", "order"]
