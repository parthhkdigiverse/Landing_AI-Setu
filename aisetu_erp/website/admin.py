from django.contrib import admin
from .models import FAQ, AllStoreType, CareerPage, ChildJobPosition, ComparisonFeature, ContactPageContent, ContactPageContent, Culture, DemoVideo, Feature, Footer, HowItWorksStep, JobDescription, JobPosition, JobSkill, LandingPageContent, LoginLink, Page, Perk, Policy, PolicySection, Problem, ReferralPerk, Section, SectionItem, StoreType, Testimonial, USPFeature, BlogCategory, BlogPost, DemoRequest, PricingSignup, ContactSubmission, JobApplication, Payment
import nested_admin

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

# @admin.register(AboutPageContent)
# class AboutPageContentAdmin(admin.ModelAdmin):

#     change_form_template = "admin/live_preview_aboutus_form.html"

# @admin.register(CareerPageContent)
# class CareerPageContentAdmin(admin.ModelAdmin):
#     change_form_template = "admin/live_preview_career_form.html"

#     # This ensures you always edit the same object
#     def has_add_permission(self, request):
#         if CareerPageContent.objects.exists():
#             return False
#         return True
    
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

@admin.register(ComparisonFeature)
class ComparisonFeatureAdmin(admin.ModelAdmin):
    list_display = ["feature_name", "has_ai_setu", "has_traditional", "is_active", "order"]
    list_editable = ["has_ai_setu", "has_traditional", "is_active", "order"]
    ordering = ["order"]  

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "is_active", "order"]
    list_editable = ["is_active", "order"]
    ordering = ["order"]
    search_fields = ["question", "answer"]

@admin.register(LoginLink)
class LoginLinkAdmin(admin.ModelAdmin):
    list_display = ["label", "url", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["label"]

@admin.register(DemoVideo)
class DemoVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "video_url", "is_active", "created_at")

@admin.register(AllStoreType)
class AllStoreTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ("email", "phone")

class CultureInline(admin.TabularInline):
    model = Culture
    extra = 1


class PerkInline(admin.TabularInline):
    model = Perk
    extra = 1


class JobPositionInline(admin.TabularInline):
    model = JobPosition
    extra = 1


@admin.register(CareerPage)
class CareerPageAdmin(admin.ModelAdmin):
    inlines = [CultureInline, PerkInline, JobPositionInline]


class JobDescriptionInline(admin.TabularInline):
    model = JobDescription
    extra = 1


class JobSkillInline(admin.TabularInline):
    model = JobSkill
    extra = 1


class ChildJobPositionInline(admin.StackedInline):

    model = ChildJobPosition
    extra = 1
    

@admin.register(ChildJobPosition)
class ChildJobPositionAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}

    inlines = [
        JobDescriptionInline,
        JobSkillInline
    ]

class SectionItemInline(nested_admin.NestedTabularInline):
    model = SectionItem
    extra = 1


# SECTION inside Page
class SectionInline(nested_admin.NestedStackedInline):
    model = Section
    extra = 1
    inlines = [SectionItemInline]


# PAGE (MAIN)
@admin.register(Page)
class PageAdmin(nested_admin.NestedModelAdmin):
    inlines = [SectionInline]
    prepopulated_fields = {"slug": ("title",)}

class PolicySectionInline(admin.TabularInline):
    model = PolicySection
    extra = 1


class PolicyAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PolicySectionInline]


admin.site.register(Policy, PolicyAdmin)

@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "contact_number", "store_type", "city"]
    search_fields = ["name", "contact_number", "city"]
    list_filter = ["store_type"]

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "created_at"]
    search_fields = ["name", "phone", "email"]
    date_hierarchy = "created_at"

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "job_position", "email", "applied_at"]
    search_fields = ["first_name", "last_name", "email", "phone"]
    list_filter = ["job_position"]
    date_hierarchy = "applied_at"

@admin.register(PricingSignup)
class PricingSignupAdmin(admin.ModelAdmin):
    list_display = ["shop_name", "owner_name", "mobile_number", "referral_code", "created_at"]
    search_fields = ["shop_name", "owner_name", "mobile_number", "referral_code"]
    date_hierarchy = "created_at"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["transaction_id", "pricing_signup", "amount", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["transaction_id", "pricing_signup__shop_name"]
    date_hierarchy = "created_at"