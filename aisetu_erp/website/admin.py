from django.contrib import admin
from .models import AboutPageContent, CareerPageContent, ContactPageContent, ContactPageContent, LandingPageContent

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
