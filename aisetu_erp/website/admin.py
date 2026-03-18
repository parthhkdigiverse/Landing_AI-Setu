import csv
from importlib import resources
import io

from django.contrib import admin
from django.http import FileResponse, HttpResponse
from .models import FAQ, AllStoreType, CareerPage, ChildJobPosition, ComparisonFeature, ContactPageContent, ContactPageContent, Culture, DemoVideo, Feature, Footer, HowItWorksStep, JobDescription, JobPosition, JobSkill, LandingPageContent, LoginLink, Page, Perk, Policy, PolicySection, Problem, ReferralPerk, Section, SectionItem, StoreType, Testimonial, USPFeature, BlogCategory, BlogPost, DemoRequestProxy, PricingSignupProxy, ContactSubmissionProxy, JobApplicationProxy, PaymentProxy
import nested_admin

from import_export.resources import ModelResource
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX, CSV
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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
    
    fieldsets = (
        ("Content", {
            "fields": ("title", "slug", "category", "featured_image", "excerpt", "content", "author", "is_published")
        }),
        ("SEO Optimization", {
            "fields": ("seo_title", "seo_description", "seo_keywords"),
            "classes": ("collapse",),
            "description": "Customize how this post appears in search engines."
        }),
    )

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

    fieldsets = (
        ("Content", {
            "fields": (
                "hero_eyebrow", "hero_title", "hero_highlighted_title", "hero_subtitle",
                "hero_highlights", "primary_cta_text", "secondary_cta_text",
                "trusted_retailers_count", "hero_stats_label", "hero_stats_value",
                "trust_item1", "trust_item2", "trust_item3", "trust_item4",
                "problem_section_label", "problem_section_title", "feature_title", "feature_title2",
                "solution_section_label", "solution_section_title", "usp_badge_text",
                "usp_title", "usp_description", "howitworks_label", "howitworks_title",
                "who_main_title", "who_title", "pricing_main_title", "pricing_main_desc",
                "pricing_label", "pricing_title", "pricing_plan_name", "pricing_old_price",
                "pricing_price", "pricing_price_suffix", "referral_main_title",
                "referral_main_desc", "referral_label", "referral_title", "join_referral",
                "comparison_title", "comparison_subtitle", "comparison_title1",
                "comparison_title2", "comparison_title3", "testimonial_label",
                "testimonial_title", "review_button", "all_reviews_title", "all_reviews_desc",
                "faq_label", "faq_title", "cta_badge", "cta_title", "cta_description",
                "cta_button_text", "cta_small_text"
            )
        }),
        ("SEO Optimization", {
            "fields": ("seo_title", "seo_description", "seo_keywords"),
            "classes": ("collapse",),
            "description": "Customize how the Home page appears in search engines."
        }),
    )

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

    fieldsets = (
        ("Hero Section", {
            "fields": ("hero_title", "hero_description")
        }),
        ("Contact Details", {
            "fields": (
                "call_title", "call_phone", "call_phone_number", "call_subtext",
                "email_title", "email_address", "email_address_link", "email_subtext",
                "visit_title", "visit_address", "visit_subtext", "visit_map_url"
            )
        }),
        ("Support & Form", {
            "fields": (
                "support_title", "support_time", "support_subtext", "form_title",
                "name_label", "name_placeholder", "phone_label", "phone_placeholder",
                "email_label", "email_placeholder", "company_label", "company_placeholder",
                "message_label", "message_placeholder", "form_button_text"
            )
        }),
        ("Why Us & CTA", {
            "fields": (
                "why_title", "why_description", "feature_1_title", "feature_2_title",
                "feature_3_title", "feature_4_title", "cta_title", "cta_description",
                "cta_button_text1", "cta_button_text2", "cta_button_text3"
            )
        }),
        ("SEO Optimization", {
            "fields": ("seo_title", "seo_description", "seo_keywords"),
            "classes": ("collapse",),
            "description": "Customize how the Contact page appears in search engines."
        }),
    )

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

    fieldsets = (
        ("Hero Content", {
            "fields": ("hero_title", "hero_subtitle")
        }),
        ("Section Titles", {
            "fields": ("culture_title", "perks_title")
        }),
        ("CTA Section", {
            "fields": ("cta_title", "cta_subtitle", "cta_button_text")
        }),
        ("SEO Optimization", {
            "fields": ("seo_title", "seo_description", "seo_keywords"),
            "classes": ("collapse",),
            "description": "Customize how the Careers page appears in search engines."
        }),
    )


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

    fieldsets = (
        ("Job Details", {
            "fields": ("career_page", "title", "slug", "location", "experience", "is_active")
        }),
        ("SEO Optimization", {
            "fields": ("seo_title", "seo_description", "seo_keywords"),
            "classes": ("collapse",),
            "description": "Customize how this specific job listing appears in search engines."
        }),
    )

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

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug")
        }),
        ("SEO Optimization", {
            "fields": ("seo_title", "seo_description", "seo_keywords"),
            "classes": ("collapse",),
            "description": "Customize how this page appears in search engines."
        }),
    )

class PolicySectionInline(admin.TabularInline):
    model = PolicySection
    extra = 1


class PolicyAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PolicySectionInline]

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "description")
        }),
        ("SEO Optimization", {
            "fields": ("seo_title", "seo_description", "seo_keywords"),
            "classes": ("collapse",),
            "description": "Customize how this policy page appears in search engines."
        }),
    )


admin.site.register(Policy, PolicyAdmin)


class ReadOnlyExportAdmin(ExportMixin, admin.ModelAdmin):
    # Default fields to export if the child class doesn't define specific ones
    export_fields = [] 

    def get_export_formats(self):
        return [XLSX, CSV]

    actions = ["export_as_pdf", "export_as_csv"]

    # 1. Logic for the 'EXPORT' Button (Top Right)
    def get_export_resource_class(self):
        model_to_use = self.model
        field_list = self.export_fields if self.export_fields else [f.name for f in model_to_use._meta.fields]
        
        class GeneratedResource(ModelResource):
            class Meta:
                model = model_to_use
                fields = field_list # Only exports these specific columns
        return GeneratedResource

    # 2. Logic for 'Export Selected to CSV'
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.model._meta.verbose_name_plural}.csv"'
        writer = csv.writer(response)
        
        # Use export_fields if defined, otherwise use all fields
        fields = self.export_fields if self.export_fields else [f.name for f in self.model._meta.fields]
        writer.writerow(fields) # Header row
        
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])
        return response
    export_as_csv.short_description = "Export Selected to CSV"

    # 3. Logic for 'Export Selected to PDF'
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []
        
        fields = self.export_fields if self.export_fields else [f.name for f in self.model._meta.fields]
        data = [fields] # Header row
        
        for obj in queryset:
            data.append([str(getattr(obj, field)) for field in fields])

        pdf_table = Table(data)
        pdf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.cadetblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
        ]))
        
        elements.append(pdf_table)
        doc.build(elements)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'{self.model._meta.model_name}.pdf')
    export_as_pdf.short_description = "Export Selected to PDF"

    # Read-only permissions
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_view_permission(self, request, obj=None): return True
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


# --- YOUR ACTUAL ADMIN REGISTRATIONS ---

@admin.register(DemoRequestProxy)
class DemoRequestAdmin(ReadOnlyExportAdmin):
    # --- 1. UI Layout ---
    list_display = ["name", "contact_number", "store_type", "city"]
    search_fields = ["name", "contact_number", "city"]
    export_fields = ["name", "contact_number", "store_type", "city"]
    list_filter = ["store_type"]

@admin.register(ContactSubmissionProxy)
class ContactSubmissionAdmin(ReadOnlyExportAdmin):
    list_display = ["name", "phone", "email", "created_at"]
    export_fields = ["name", "phone", "email", "OfficeAddress", "Message"]
    search_fields = ["name", "phone", "email"]
    date_hierarchy = "created_at"

@admin.register(JobApplicationProxy)
class JobApplicationAdmin(ReadOnlyExportAdmin):
    list_display = ["first_name", "last_name", "job_position", "email", "applied_at"]
    export_fields = ["first_name", "last_name", "email", "phone", "job_position", "experience", "available_to_join", "current_salary", "expected_salary", "location", "applied_at"]
    search_fields = ["first_name", "last_name", "email", "phone"]
    list_filter = ["job_position"]
    date_hierarchy = "applied_at"

@admin.register(PricingSignupProxy)
class PricingSignupAdmin(ReadOnlyExportAdmin):
    list_display = ["shop_name", "owner_name", "mobile_number", "referral_code", "created_at"]
    export_fields = ["shop_name", "owner_name", "mobile_number", "referral_code", "total_referrals"]
    search_fields = ["shop_name", "owner_name", "mobile_number", "referral_code"]
    date_hierarchy = "created_at"

@admin.register(PaymentProxy)
class PaymentAdmin(ReadOnlyExportAdmin):
    list_display = ["transaction_id", "pricing_signup", "amount", "status", "created_at"]
    export_fields = ["transaction_id", "pricing_signup", "amount", "status"]
    list_filter = ["status"]
    search_fields = ["transaction_id", "pricing_signup__shop_name"]
    readonly_fields = ["response_data"]
    date_hierarchy = "created_at"
