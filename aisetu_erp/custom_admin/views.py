from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random, string, json
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.apps import apps
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from functools import wraps

from django.forms import inlineformset_factory, modelformset_factory
from django.http import FileResponse
import csv, io
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from website.models import AdminUser, DemoRequest, PricingSignup, Payment, ContactSubmission
from website.models import CareerPage, Culture, Perk, JobPosition
from website.models import (
    LandingPageContent, Problem, Feature, USPFeature, 
    HowItWorksStep, StoreType, ReferralPerk, Testimonial, 
    ComparisonFeature, FAQ, TrustItem, PricingFeature,
    ChildJobPosition, JobDescription, JobSkill,
    PricingContent, ReferralProgramContent, TrustContent,
    ChallengeContent, SolutionContent, USPContent,
    HowItWorksContent, WhoIsThisForContent, TestimonialContent,
    ComparisonContent, FAQContent, CTAContent, ContactPageContent, 
    HeroContent, AboutPageContent, AboutUsServeItem, AboutUsWhyChooseItem, Policy, PolicySection, AllStoreType, Footer, SocialLink
)
SocialLinkFormSet = inlineformset_factory(Footer, SocialLink, fields='__all__', extra=1, can_delete=True)
ReferralPerkFormSet = inlineformset_factory(ReferralProgramContent, ReferralPerk, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)

# Challenge Formsets
ChallengeProblemFormSet = inlineformset_factory(ChallengeContent, Problem, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
SolutionFeatureFormSet = inlineformset_factory(SolutionContent, Feature, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
USPContentFormSet = inlineformset_factory(USPContent, USPFeature, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
HIWStepFormSet = inlineformset_factory(HowItWorksContent, HowItWorksStep, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
StoreTypeContentFormSet = inlineformset_factory(WhoIsThisForContent, StoreType, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
TestimonialContentFormSet = inlineformset_factory(TestimonialContent, Testimonial, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
ComparisonContentFormSet = inlineformset_factory(ComparisonContent, ComparisonFeature, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
FAQContentFormSet = inlineformset_factory(FAQContent, FAQ, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
TrustContentFormSet = inlineformset_factory(TrustContent, TrustItem, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)
PricingFeatureFormSet = inlineformset_factory(PricingContent, PricingFeature, fk_name='landing_page', fields='__all__', extra=1, can_delete=True)

# Career & Job Formsets
CultureFormSet = inlineformset_factory(CareerPage, Culture, fk_name='career_page', fields='__all__', extra=1, can_delete=True)
PerkFormSet = inlineformset_factory(CareerPage, Perk, fk_name='career_page', fields='__all__', extra=1, can_delete=True)
OpenPositionFormSet = inlineformset_factory(CareerPage, ChildJobPosition, fk_name='career_page', fields=['title', 'slug', 'location', 'experience', 'total_positions', 'work_place'], extra=1, can_delete=True)
JobDescriptionFormSet = inlineformset_factory(ChildJobPosition, JobDescription, fk_name='job', fields='__all__', extra=1, can_delete=True)
JobSkillFormSet = inlineformset_factory(ChildJobPosition, JobSkill, fk_name='job', fields='__all__', extra=1, can_delete=True)

# About & Policy Formsets
ServeItemFormSet = inlineformset_factory(AboutPageContent, AboutUsServeItem, fk_name='about_page', fields='__all__', extra=1, can_delete=True)
WhyChooseItemFormSet = inlineformset_factory(AboutPageContent, AboutUsWhyChooseItem, fk_name='about_page', fields='__all__', extra=1, can_delete=True)
PolicySectionFormSet = inlineformset_factory(Policy, PolicySection, fk_name='policy', fields='__all__', extra=1, can_delete=True)

AllStoreTypeFormSet = modelformset_factory(AllStoreType, fields=('name', 'is_active'), extra=1, can_delete=True)

def custom_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('custom_admin:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def custom_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            admin = AdminUser.objects.get(email=email)
            if admin.password == password:
                request.session['is_admin'] = True
                request.session['admin_email'] = email
                return redirect('custom_admin:dashboard')
            else:
                return render(request, 'custom_admin/login.html', {'error': 'Invalid Credentials'})
        except AdminUser.DoesNotExist:
            return render(request, 'custom_admin/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'custom_admin/login.html')

def custom_logout(request):
    request.session.flush()
    return redirect('custom_admin:login')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            admin = AdminUser.objects.get(email=email)
            otp = ''.join(random.choices(string.digits, k=6))
            admin.otp = otp
            admin.otp_created_at = timezone.now()
            admin.save()
            
            # Send Email
            from django.conf import settings
            subject = 'Your Admin Password Reset OTP'
            message = f'Your OTP for password reset is: {otp}. It is valid for 10 minutes.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                return render(request, 'custom_admin/forgot_password.html', {'error': f'Failed to send email: {str(e)}. Please ensure your Google App Password is correct in settings.py.'})

            request.session['reset_email'] = email
            return redirect('custom_admin:verify_otp')
        except AdminUser.DoesNotExist:
            return render(request, 'custom_admin/forgot_password.html', {'error': 'Admin user not found.'})
            
    return render(request, 'custom_admin/forgot_password.html')

def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('custom_admin:forgot_password')
        
    if request.method == "POST":
        otp_input = request.POST.get('otp')
        try:
            admin = AdminUser.objects.get(email=email)
            if admin.otp == otp_input:
                # Check expiry (10 minutes)
                if timezone.now() < admin.otp_created_at + timedelta(minutes=10):
                    request.session['otp_verified'] = True
                    return redirect('custom_admin:reset_password')
                else:
                    return render(request, 'custom_admin/verify_otp.html', {'error': 'OTP has expired.'})
            else:
                return render(request, 'custom_admin/verify_otp.html', {'error': 'Invalid OTP.'})
        except AdminUser.DoesNotExist:
            return redirect('custom_admin:forgot_password')
            
    return render(request, 'custom_admin/verify_otp.html', {'email': email})

def reset_password(request):
    email = request.session.get('reset_email')
    verified = request.session.get('otp_verified')
    
    if not email or not verified:
        return redirect('custom_admin:forgot_password')
        
    if request.method == "POST":
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            return render(request, 'custom_admin/reset_password.html', {'error': 'Passwords do not match.'})
            
        try:
            admin = AdminUser.objects.get(email=email)
            admin.password = new_password
            admin.otp = None
            admin.otp_created_at = None
            admin.save()
            
            # Clear session
            del request.session['reset_email']
            del request.session['otp_verified']
            
            return render(request, 'custom_admin/login.html', {'success': 'Password updated successfully. Please login.'})
        except AdminUser.DoesNotExist:
            return redirect('custom_admin:forgot_password')
            
    return render(request, 'custom_admin/reset_password.html')

@custom_admin_required
def dashboard(request):
    from website.models import JobApplication
    context = {
        'demo_count': DemoRequest.objects.count(),
        'signup_count': PricingSignup.objects.count(),
        'payment_count': Payment.objects.count(),
        'contact_count': ContactSubmission.objects.count(),
        'job_application_count': JobApplication.objects.count(),
        'policy_count': Policy.objects.count(),
    }
    return render(request, 'custom_admin/dashboard.html', context)

@custom_admin_required
def edit_singleton(request, model_name):
    model = apps.get_model('website', model_name)
    obj = model.objects.first()
    if not obj:
        obj = model.objects.create()
    
    url = reverse('custom_admin:model_update', kwargs={'app_label': 'website', 'model_name': model_name, 'pk': obj.pk})
    query_string = request.GET.urlencode()
    if query_string:
        url += '?' + query_string
    return redirect(url)

class AdminRequiredMixin:
    @method_decorator(custom_admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class DynamicModelMixin:
    def get_model(self):
        app_label = self.kwargs.get('app_label', 'website')
        model_name = self.kwargs.get('model_name')
        return apps.get_model(app_label, model_name)
    def get_queryset(self):
        return self.get_model().objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.get_model()
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['app_label'] = self.kwargs.get('app_label', 'website')
        context['model_slug'] = self.kwargs.get('model_name')
        context['model_class_name'] = model.__name__
        if hasattr(self, 'object_list'):
            fields = [f for f in model._meta.fields if f.name not in ['id', '_id', 'password']]
            context['fields'] = fields[:15]
        return context

class CustomAdminListView(AdminRequiredMixin, DynamicModelMixin, ListView):
    template_name = 'custom_admin/model_list.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get('model_name', '').lower().strip()
        scheme, host = self.request.scheme, self.request.get_host()
        base_url = f"{scheme}://{host}"
        if 'referralperk' in model_name: context.update({'preview_url': f"{base_url}/", 'scroll_target': 'referral'})
        elif 'challengecontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=problem", 'scroll_target': 'problem'})
        elif 'solutioncontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=solution", 'scroll_target': 'solution'})
        elif 'uspcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=usp", 'scroll_target': 'usp'})
        elif 'howitworkscontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=how-it-works", 'scroll_target': 'how-it-works'})
        elif 'whoisthisforcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=who-is-this-for", 'scroll_target': 'who-is-this-for'})
        elif 'testimonialcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=testimonials", 'scroll_target': 'testimonials'})
        elif 'comparisoncontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=comparison", 'scroll_target': 'comparison'})
        elif 'faqcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=faq", 'scroll_target': 'faq'})
        
        readonly_models = ['demorequest', 'jobapplication', 'pricingsignup', 'contactsubmission', 'payment']
        context['is_readonly'] = model_name in readonly_models
        if context['is_readonly']:
            headers = [f.verbose_name.title() for f in context.get('fields', [])]
            
            # Special handling for Payment to extract specific JSON fields
            if model_name == 'payment':
                # Remove 'Response Data'
                try:
                    rd_idx = headers.index('Response Data')
                    headers.pop(rd_idx)
                except ValueError:
                    rd_idx = None
                
                # Remove 'Invoice'
                try:
                    inv_idx = headers.index('Invoice')
                    headers.pop(inv_idx)
                except ValueError:
                    inv_idx = None
                
                headers.extend(['Merchant Id', 'Merchant Transaction Id', 'State'])
            
            context['headers'] = headers
            rows = []
            for obj in context.get('object_list', []):
                row_data = []
                for f in context.get('fields', []):
                    # Skip the raw response_data and invoice if it's payment
                    if model_name == 'payment' and f.name in ['response_data', 'invoice']:
                        continue
                        
                    val = getattr(obj, f.name, '')
                    if val and hasattr(val, 'url'):
                        val = f"<a href='javascript:void(0)' data-file-url='{val.url}' class='view-file-btn text-decoration-none'><i class='bi bi-file-earmark-text'></i> View</a>"
                    else: val = str(val) if val is not None else ''
                    row_data.append(val)
                
                # Append the extracted fields for payment
                if model_name == 'payment':
                    rd = getattr(obj, 'response_data', {}) or {}
                    # Ensure rd is a dict
                    if isinstance(rd, str):
                        import json
                        try: rd = json.loads(rd)
                        except: rd = {}
                    
                    data = rd.get('data', {}) if isinstance(rd, dict) else {}
                    row_data.append(str(data.get('merchantId', '')))
                    row_data.append(str(data.get('merchantTransactionId', '')))
                    row_data.append(str(data.get('state', '')))
                
                rows.append({'pk': obj.pk, 'data': row_data})
            context['tabular_rows'] = rows
        return context

@custom_admin_required
def export_model_csv(request, app_label, model_name):
    model = apps.get_model(app_label, model_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model._meta.verbose_name_plural}.csv"'
    writer = csv.writer(response)
    
    # Exclude id, password and _id
    fields = [f for f in model._meta.fields if f.name not in ['id', 'password', '_id']]
    headers = [f.verbose_name.title() for f in fields]
    
    # Special handling for Payment to extract specific JSON fields
    is_payment = model_name.lower() == 'payment'
    if is_payment:
        try: headers.remove('Response Data')
        except: pass
        try: headers.remove('Invoice')
        except: pass
        headers.extend(['Merchant Id', 'Merchant Transaction Id', 'State'])
        
    writer.writerow(headers)
    
    for obj in model.objects.all():
        row_data = []
        for f in fields:
            if is_payment and f.name in ['response_data', 'invoice']:
                continue
            val = getattr(obj, f.name, '')
            if val and hasattr(val, 'url'):
                val = request.build_absolute_uri(val.url)
            row_data.append(str(val) if val is not None else '')
            
        if is_payment:
            rd = getattr(obj, 'response_data', {}) or {}
            if isinstance(rd, str):
                try: rd = json.loads(rd)
                except: rd = {}
            data = rd.get('data', {}) if isinstance(rd, dict) else {}
            row_data.append(str(data.get('merchantId', '')))
            row_data.append(str(data.get('merchantTransactionId', '')))
            row_data.append(str(data.get('state', '')))
            
        writer.writerow(row_data)
    return response

@custom_admin_required
def export_model_pdf(request, app_label, model_name):
    model = apps.get_model(app_label, model_name)
    buffer = io.BytesIO()
    
    # Use larger page size for more columns if needed
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), 
                            rightMargin=20, leftMargin=20, 
                            topMargin=40, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    
    # 1. Header Section
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center
    title_style.textColor = colors.HexColor("#1F2E4D")
    elements.append(Paragraph(f"AI-SETU ERP - {model._meta.verbose_name_plural.title()}", title_style))
    elements.append(Spacer(1, 4))
    
    # 2. Metadata Section
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1 # Center
    )
    gen_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Official Data Export | Generated on: {gen_time} | Total Records: {model.objects.count()}", meta_style))
    elements.append(Spacer(1, 20))
    
    # 3. Table Data Preparation
    fields = [f for f in model._meta.fields if f.name not in ['id', 'password', '_id']]
    headers = [f.verbose_name.title() for f in fields]
    
    is_payment = model_name.lower() == 'payment'
    if is_payment:
        try: headers.remove('Response Data')
        except: pass
        try: headers.remove('Invoice')
        except: pass
        headers.extend(['Merchant Id', 'Merchant Transaction Id', 'State'])
    
    data_list = [headers]
    for obj in model.objects.all():
        row_data = []
        for f in fields:
            if is_payment and f.name in ['response_data', 'invoice']:
                continue
            val = getattr(obj, f.name, '')
            if val and hasattr(val, 'url'):
                val = "File Attached"
            row_data.append(str(val) if val is not None else '')
            
        if is_payment:
            rd = getattr(obj, 'response_data', {}) or {}
            if isinstance(rd, str):
                try: rd = json.loads(rd)
                except: rd = {}
            data_dict = rd.get('data', {}) if isinstance(rd, dict) else {}
            row_data.append(str(data_dict.get('merchantId', '')))
            row_data.append(str(data_dict.get('merchantTransactionId', '')))
            row_data.append(str(data_dict.get('state', '')))
        data_list.append(row_data)

    # 4. Table Styling
    # Adjust column widths based on the number of columns
    num_cols = len(headers)
    available_width = doc.width
    col_width = available_width / num_cols if num_cols > 0 else 50
    
    table = Table(data_list, repeatRows=1, colWidths=[col_width] * num_cols)
    
    style_opts = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1F2E4D")), # Dark blue header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    
    # Add alternating row colors for better readability
    for i in range(1, len(data_list)):
        if i % 2 == 0:
            style_opts.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#F8FAFC")))
            
    table.setStyle(TableStyle(style_opts))
    elements.append(table)
    
    # 5. Page Numbering Function
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setStrokeColor(colors.lightgrey)
        canvas.line(20, 40, doc.pagesize[0] - 20, 40) # Horizontal line at bottom
        
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawRightString(doc.pagesize[0] - 20, 25, text)
        canvas.drawString(20, 25, "AI-SETU Official Data Export - Confidential")
        canvas.restoreState()

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{model._meta.model_name}_export_{timezone.now().strftime("%Y%m%d")}.pdf')

class CustomAdminCreateView(AdminRequiredMixin, DynamicModelMixin, CreateView):
    template_name = 'custom_admin/model_form.html'
    def get_form_class(self):
        from django.forms import modelform_factory
        model, model_name = self.get_model(), self.kwargs.get('model_name', '').lower()
        hero_fields = ['hero_eyebrow', 'hero_title', 'hero_highlighted_title', 'hero_subtitle', 'hero_highlights', 'primary_cta_text', 'secondary_cta_text', 'trusted_retailers_count', 'hero_stats_label', 'hero_stats_value']
        cta_fields = ['cta_badge', 'cta_title', 'cta_description', 'cta_button_text', 'cta_small_text']
        seo_fields = ['seo_title', 'seo_description', 'seo_keywords']
        
        about_hero_fields = ['about_label', 'hero_title', 'hero_description']
        about_story_fields = ['about_heading', 'about_image', 'about_description_1', 'about_description_2', 'about_description_3']
        about_mission_fields = ['mission_title', 'mission_description']
        about_why_fields = ['why_choose_title']
        about_serve_fields = ['serve_title', 'serve_subtitle']
        about_cta_fields = ['cta_title', 'cta_description', 'cta_button_text']
        
        if model_name == 'pricingcontent':
            fields = ['pricing_main_title', 'pricing_main_desc', 'pricing_label', 'pricing_title', 'pricing_plan_name', 'pricing_old_price', 'pricing_price', 'pricing_price_suffix']
        elif model_name == 'careerherocontent': fields = ['hero_title', 'hero_subtitle']
        elif model_name == 'careerculturecontent': fields = ['culture_title']
        elif model_name == 'careerperkscontent': fields = ['perks_title']
        elif model_name == 'careerjobscontent': fields = []
        elif model_name == 'careerctacontent': fields = ['cta_title', 'cta_subtitle', 'cta_button_text']
        elif model_name == 'aboutherocontent': fields = about_hero_fields
        elif model_name == 'aboutstorycontent': fields = about_story_fields + seo_fields
        elif model_name == 'aboutmissioncontent': fields = about_mission_fields
        elif model_name == 'aboutwhychoosecontent': fields = about_why_fields
        elif model_name == 'aboutservecontent': fields = about_serve_fields
        elif model_name == 'aboutctacontent': fields = about_cta_fields
        elif model_name == 'aboutpagecontent': fields = about_hero_fields + about_story_fields + about_mission_fields + about_why_fields + about_serve_fields + about_cta_fields + seo_fields
        elif model_name == 'landingpagecontent': fields = hero_fields + seo_fields
        elif model_name == 'ctacontent': fields = cta_fields
        elif model_name == 'referralprogramcontent': fields = ['referral_main_title', 'referral_main_desc', 'referral_label', 'referral_title', 'join_referral']
        elif model_name == 'challengecontent': fields = ['problem_section_label', 'problem_section_title']
        elif model_name == 'solutioncontent': fields = ['feature_title', 'feature_title2', 'solution_section_label', 'solution_section_title']
        elif model_name == 'uspcontent': fields = ['usp_badge_text', 'usp_title', 'usp_description']
        elif model_name == 'howitworkscontent': fields = ['howitworks_label', 'howitworks_title']
        elif model_name == 'whoisthisforcontent': fields = ['who_main_title', 'who_title']
        elif model_name == 'testimonialcontent': fields = ['testimonial_label', 'testimonial_title', 'review_button', 'all_reviews_title', 'all_reviews_desc']
        elif model_name == 'comparisoncontent': fields = ['comparison_title', 'comparison_subtitle', 'comparison_title1', 'comparison_title2', 'comparison_title3']
        elif model_name == 'faqcontent': fields = ['faq_label', 'faq_title']
        elif model_name == 'trustcontent': fields = []
        else: fields = '__all__'
        return modelform_factory(model, fields=fields)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get('model_name', '').lower().strip()
        # Formset logic
        if model_name in ['careerpage', 'careerherocontent', 'careerculturecontent', 'careerperkscontent', 'careerjobscontent', 'careerctacontent']:
            if model_name == 'careerherocontent': section = 'hero'
            elif model_name == 'careerculturecontent': section = 'culture'
            elif model_name == 'careerperkscontent': section = 'perks'
            elif model_name == 'careerjobscontent': section = 'jobs'
            elif model_name == 'career Jobscontent': section = 'jobs'
            elif model_name == 'careerctacontent': section = 'cta'
            else: section = 'all'
            context.update({'is_career_page': True, 'career_section': section})
            if section and section != 'all':
                context['scroll_target'] = 'open_positions' if section == 'jobs' else section
            if section in ['all', 'culture']: context['culture_formset'] = CultureFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None))
            if section in ['all', 'perks']: context['perk_formset'] = PerkFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None))
            if section in ['all', 'jobs']: context['job_formset'] = OpenPositionFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None))
        elif 'childjobposition' in model_name: context.update({'is_child_job_position': True, 'description_formset': JobDescriptionFormSet(self.request.POST or None, self.request.FILES or None), 'skill_formset': JobSkillFormSet(self.request.POST or None, self.request.FILES or None)})
        elif model_name in ['aboutpagecontent', 'aboutherocontent', 'aboutstorycontent', 'aboutmissioncontent', 'aboutwhychoosecontent', 'aboutservecontent', 'aboutctacontent']:
            if model_name == 'aboutherocontent': section = 'hero'
            elif model_name == 'aboutstorycontent': section = 'story'
            elif model_name == 'aboutmissioncontent': section = 'mission'
            elif model_name == 'aboutwhychoosecontent': section = 'why'
            elif model_name == 'aboutservecontent': section = 'serve'
            elif model_name == 'aboutctacontent': section = 'cta'
            else: section = 'all'
            context.update({
                'is_about_page': True,
                'about_section': section,
                'about_hero_fields': ['about_label', 'hero_title', 'hero_description'],
                'about_story_fields': ['about_heading', 'about_image', 'about_description_1', 'about_description_2', 'about_description_3'],
                'about_mission_fields': ['mission_title', 'mission_description'],
                'about_why_fields': ['why_choose_title'],
                'about_serve_fields': ['serve_title', 'serve_subtitle'],
                'about_cta_fields': ['cta_title', 'cta_description', 'cta_button_text'],
                'seo_fields': ['seo_title', 'seo_description', 'seo_keywords'],
                'serve_formset': ServeItemFormSet(self.request.POST or None, self.request.FILES or None),
                'why_formset': WhyChooseItemFormSet(self.request.POST or None, self.request.FILES or None)
            })
        elif 'referralprogramcontent' in model_name: context.update({'is_referral_program': True, 'referral_formset': ReferralPerkFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'challengecontent' in model_name: context.update({'is_challenge_section': True, 'challenge_formset': ChallengeProblemFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'solutioncontent' in model_name: context.update({'is_solution_section': True, 'solution_formset': SolutionFeatureFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'uspcontent' in model_name: context.update({'is_usp_section': True, 'usp_formset': USPContentFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'howitworkscontent' in model_name: context.update({'is_hiw_section': True, 'hiw_formset': HIWStepFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'whoisthisforcontent' in model_name: context.update({'is_who_section': True, 'who_formset': StoreTypeContentFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'testimonialcontent' in model_name: context.update({'is_testimonial_section': True, 'testimonial_formset': TestimonialContentFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'comparisoncontent' in model_name: context.update({'is_comparison_section': True, 'comparison_formset': ComparisonContentFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'faqcontent' in model_name: context.update({'is_faq_section': True, 'faq_formset': FAQContentFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None))})
        elif 'trustcontent' in model_name: context.update({'is_trust_section': True, 'trust_formset': TrustContentFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None))})
        elif 'pricingcontent' in model_name: context.update({'is_pricing_section': True, 'pricing_formset': PricingFeatureFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None))})
        elif 'policy' == model_name: context.update({'is_policy': True, 'section_formset': PolicySectionFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'footer' in model_name: context.update({'is_footer_page': True, 'social_formset': SocialLinkFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'landingpagecontent' in model_name:
            context.update({'is_landing_page': True})
            if self.request.GET.get('master') == '1':
                context.update({
                    'is_master_editor': True,
                    'is_challenge_section': True, 'challenge_formset': ChallengeProblemFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_solution_section': True, 'solution_formset': SolutionFeatureFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_usp_section': True, 'usp_formset': USPContentFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_hiw_section': True, 'hiw_formset': HIWStepFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_who_section': True, 'who_formset': StoreTypeContentFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_pricing_section': True, 'pricing_formset': PricingFeatureFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_referral_program': True, 'referral_formset': ReferralPerkFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_testimonial_section': True, 'testimonial_formset': TestimonialContentFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_comparison_section': True, 'comparison_formset': ComparisonContentFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_faq_section': True, 'faq_formset': FAQContentFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                    'is_trust_section': True, 'trust_formset': TrustContentFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, 'object', None)),
                })
        
        # Preview URL logic
        scheme, host = self.request.scheme, self.request.get_host()
        base_url = f"{scheme}://{host}"
        if model_name in ['aboutpagecontent', 'aboutherocontent', 'aboutstorycontent', 'aboutmissioncontent', 'aboutwhychoosecontent', 'aboutservecontent', 'aboutctacontent']:
            context['preview_url'] = f"{base_url}/about?is_preview=1"
            if section and section != 'all':
                context['preview_url'] += f"&section={section}"
        elif 'landingpagecontent' in model_name: context['preview_url'] = f"{base_url}/?is_preview=1"
        elif model_name == 'ctacontent': context.update({'preview_url': f"{base_url}/?is_preview=1&section=cta", 'scroll_target': 'cta'})
        elif 'trustcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=trusted-retailers", 'scroll_target': 'trusted-retailers'})
        elif 'referralprogramcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=referral", 'scroll_target': 'referral'})
        elif 'challengecontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=problem", 'scroll_target': 'problem'})
        elif 'solutioncontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=solution", 'scroll_target': 'solution'})
        elif 'uspcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=usp", 'scroll_target': 'usp'})
        elif 'howitworkscontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=how-it-works", 'scroll_target': 'how-it-works'})
        elif 'whoisthisforcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=who-is-this-for", 'scroll_target': 'who-is-this-for'})
        elif 'testimonialcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=testimonials", 'scroll_target': 'testimonials'})
        elif 'comparisoncontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=comparison", 'scroll_target': 'comparison'})
        elif 'faqcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=faq", 'scroll_target': 'faq'})
        elif 'pricingcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=pricing", 'scroll_target': 'pricing'})
        elif model_name in ['careerpage', 'careerherocontent', 'careerculturecontent', 'careerperkscontent', 'careerjobscontent', 'careerctacontent']:
            context['preview_url'] = f"{base_url}/career"
            if section and section != 'all': 
                context['preview_url'] += f"?is_preview=1&section={section}"
                context['scroll_target'] = 'open_positions' if section == 'jobs' else section
        elif 'contactpagecontent' in model_name: context['preview_url'] = f"{base_url}/contact"
        elif 'childjobposition' in model_name: context.update({'preview_url': f"{base_url}/career/new-job?is_preview=1"})
        elif 'policy' == model_name: 
            # For create view, we might not have a slug yet, use placeholder
            context['preview_url'] = f"{base_url}/policy/new-policy"
        elif 'footer' in model_name: context.update({'is_footer_page': True, 'social_formset': SocialLinkFormSet(self.request.POST or None, self.request.FILES or None), 'preview_url': f"{base_url}/?is_preview=1&section=footer", 'scroll_target': 'master-footer'})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        model_name = self.kwargs.get('model_name', '').lower()
        formset_keys = {
            'careerpage': ['culture_formset', 'perk_formset', 'job_formset'],
            'careerculturecontent': ['culture_formset'],
            'careerperkscontent': ['perk_formset'],
            'careerjobscontent': ['job_formset'],
            'childjobposition': ['description_formset', 'skill_formset'],
            'aboutpagecontent': ['serve_formset', 'why_formset'],
            'aboutwhychoosecontent': ['why_formset'],
            'aboutservecontent': ['serve_formset'],
            'referralprogramcontent': ['referral_formset'],
            'challengecontent': ['challenge_formset'],
            'solutioncontent': ['solution_formset'],
            'uspcontent': ['usp_formset'],
            'howitworkscontent': ['hiw_formset'],
            'whoisthisforcontent': ['who_formset'],
            'testimonialcontent': ['testimonial_formset'],
            'comparisoncontent': ['comparison_formset'],
            'faqcontent': ['faq_formset'],
            'trustcontent': ['trust_formset'],
            'pricingcontent': ['pricing_formset'],
            'landingpagecontent': ['challenge_formset', 'solution_formset', 'usp_formset', 'hiw_formset', 'who_formset', 'pricing_formset', 'referral_formset', 'testimonial_formset', 'comparison_formset', 'faq_formset', 'trust_formset'],
            'policy': ['section_formset'],
            'footer': ['social_formset'],
        }
        if model_name in formset_keys:
            formsets = [context[k] for k in formset_keys[model_name] if k in context]
            if all(fs.is_valid() for fs in formsets):
                self.object = form.save()
                for fs in formsets: fs.instance = self.object; fs.save()
                return super().form_valid(form)
            else: return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('custom_admin:model_list', kwargs={'app_label': self.kwargs.get('app_label', 'website'), 'model_name': self.kwargs.get('model_name')})

class CustomAdminUpdateView(AdminRequiredMixin, DynamicModelMixin, UpdateView):
    template_name = 'custom_admin/model_form.html'
    
    def get_form_class(self):
        from django.forms import modelform_factory
        model, model_name = self.get_model(), self.kwargs.get('model_name', '').lower().strip()
        section = self.request.GET.get('section')
        
        # --- Field Definitions ---
        hero_fields = ['hero_eyebrow', 'hero_title', 'hero_highlighted_title', 'hero_subtitle', 'hero_highlights', 'primary_cta_text', 'secondary_cta_text', 'trusted_retailers_count', 'hero_stats_label', 'hero_stats_value']
        cta_fields = ['cta_badge', 'cta_title', 'cta_description', 'cta_button_text', 'cta_small_text']
        seo_fields = ['seo_title', 'seo_description', 'seo_keywords']
        
        about_hero_fields = ['about_label', 'hero_title', 'hero_description']
        about_story_fields = ['about_heading', 'about_image', 'about_description_1', 'about_description_2', 'about_description_3']
        about_mission_fields = ['mission_title', 'mission_description']
        about_why_fields = ['why_choose_title']
        about_serve_fields = ['serve_title', 'serve_subtitle']
        about_cta_fields = ['cta_title', 'cta_description', 'cta_button_text']
        
        contact_hero = ['hero_title', 'hero_description']
        contact_cards = ['call_title', 'call_phone', 'call_phone_number', 'call_subtext', 'email_title', 'email_address', 'email_address_link', 'email_subtext', 'visit_title', 'visit_address', 'visit_subtext', 'visit_map_url', 'support_title', 'support_time', 'support_subtext']
        contact_form = ['form_title', 'name_label', 'name_placeholder', 'phone_label', 'phone_placeholder', 'email_label', 'email_placeholder', 'company_label', 'company_placeholder', 'message_label', 'message_placeholder', 'form_button_text']
        contact_why = ['why_title', 'why_description', 'feature_1_title', 'feature_2_title', 'feature_3_title', 'feature_4_title']
        contact_cta = ['cta_title', 'cta_description', 'cta_button_text1', 'cta_button_text2', 'cta_button_text3']
        
        if model_name == 'pricingcontent':
            fields = ['pricing_main_title', 'pricing_main_desc', 'pricing_label', 'pricing_title', 'pricing_plan_name', 'pricing_old_price', 'pricing_price', 'pricing_price_suffix']
        elif model_name == 'careerherocontent': fields = ['hero_title', 'hero_subtitle']
        elif model_name == 'careerculturecontent': fields = ['culture_title']
        elif model_name == 'careerperkscontent': fields = ['perks_title']
        elif model_name == 'careerjobscontent': fields = []
        elif model_name == 'careerctacontent': fields = ['cta_title', 'cta_subtitle', 'cta_button_text']
        elif model_name == 'aboutherocontent': fields = about_hero_fields
        elif model_name == 'aboutstorycontent': fields = about_story_fields + seo_fields
        elif model_name == 'aboutmissioncontent': fields = about_mission_fields
        elif model_name == 'aboutwhychoosecontent': fields = about_why_fields
        elif model_name == 'aboutservecontent': fields = about_serve_fields
        elif model_name == 'aboutctacontent': fields = about_cta_fields
        elif model_name == 'aboutpagecontent': fields = about_hero_fields + about_story_fields + about_mission_fields + about_why_fields + about_serve_fields + about_cta_fields + seo_fields
        elif model_name == 'landingpagecontent': fields = hero_fields + seo_fields
        elif model_name == 'ctacontent': fields = cta_fields
        elif model_name == 'referralprogramcontent': fields = ['referral_main_title', 'referral_main_desc', 'referral_label', 'referral_title', 'join_referral']
        elif model_name == 'challengecontent': fields = ['problem_section_label', 'problem_section_title']
        elif model_name == 'solutioncontent': fields = ['feature_title', 'feature_title2', 'solution_section_label', 'solution_section_title']
        elif model_name == 'uspcontent': fields = ['usp_badge_text', 'usp_title', 'usp_description']
        elif model_name == 'howitworkscontent': fields = ['howitworks_label', 'howitworks_title']
        elif model_name == 'whoisthisforcontent': fields = ['who_main_title', 'who_title']
        elif model_name == 'testimonialcontent': fields = ['testimonial_label', 'testimonial_title', 'review_button', 'all_reviews_title', 'all_reviews_desc']
        elif model_name == 'comparisoncontent': fields = ['comparison_title', 'comparison_subtitle', 'comparison_title1', 'comparison_title2', 'comparison_title3']
        elif model_name == 'faqcontent': fields = ['faq_label', 'faq_title']
        elif model_name == 'trustcontent': fields = []
        
        elif model_name == 'contactpagecontent':
            if section == 'hero': fields = contact_hero
            elif section == 'contact_cards': fields = contact_cards
            elif section == 'form': fields = contact_form
            elif section == 'why_choose': fields = contact_why
            elif section == 'cta': fields = contact_cta
            elif section == 'seo': fields = seo_fields
            else: fields = contact_hero + contact_cards + contact_form + contact_why + contact_cta + seo_fields
            
        elif model_name == 'aboutpagecontent':
            if section == 'hero': fields = about_hero_fields
            elif section == 'content': fields = about_story_fields
            elif section == 'mission': fields = about_mission_fields
            elif section == 'why_choose': fields = about_why_fields
            elif section == 'serve': fields = about_serve_fields
            elif section == 'cta': fields = about_cta_fields
            else: fields = about_hero_fields + about_story_fields + about_mission_fields + about_why_fields + about_serve_fields + about_cta_fields + seo_fields
        
        else: fields = '__all__'
        
        return modelform_factory(model, fields=fields)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.request.GET.get('section')
        context['section_param'] = section
        model_name = self.kwargs.get('model_name', '').lower().strip()
        if model_name in ['careerpage', 'careerherocontent', 'careerculturecontent', 'careerperkscontent', 'careerjobscontent', 'careerctacontent']:
            if model_name == 'careerherocontent': section = 'hero'
            elif model_name == 'careerculturecontent': section = 'culture'
            elif model_name == 'careerperkscontent': section = 'perks'
            elif model_name == 'careerjobscontent': section = 'jobs'
            elif model_name == 'careerctacontent': section = 'cta'
            else: section = 'all'
            context.update({'is_career_page': True, 'career_section': section})
            if section in ['all', 'culture']: context['culture_formset'] = CultureFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)
            if section in ['all', 'perks']: context['perk_formset'] = PerkFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)
            if section in ['all', 'jobs']: context['job_formset'] = OpenPositionFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)
        elif 'childjobposition' in model_name: context.update({'is_child_job_position': True, 'description_formset': JobDescriptionFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object), 'skill_formset': JobSkillFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif model_name in ['aboutpagecontent', 'aboutherocontent', 'aboutstorycontent', 'aboutmissioncontent', 'aboutwhychoosecontent', 'aboutservecontent', 'aboutctacontent']:
            if model_name == 'aboutherocontent': section = 'hero'
            elif model_name == 'aboutstorycontent': section = 'story'
            elif model_name == 'aboutmissioncontent': section = 'mission'
            elif model_name == 'aboutwhychoosecontent': section = 'why'
            elif model_name == 'aboutservecontent': section = 'serve'
            elif model_name == 'aboutctacontent': section = 'cta'
            else: section = 'all'
            context.update({
                'is_about_page': True,
                'about_section': section,
                'about_hero_fields': ['about_label', 'hero_title', 'hero_description'],
                'about_story_fields': ['about_heading', 'about_image', 'about_description_1', 'about_description_2', 'about_description_3'],
                'about_mission_fields': ['mission_title', 'mission_description'],
                'about_why_fields': ['why_choose_title'],
                'about_serve_fields': ['serve_title', 'serve_subtitle'],
                'about_cta_fields': ['cta_title', 'cta_description', 'cta_button_text'],
                'seo_fields': ['seo_title', 'seo_description', 'seo_keywords'],
                'serve_formset': ServeItemFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                'why_formset': WhyChooseItemFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)
            })
        elif 'referralprogramcontent' in model_name: context.update({'is_referral_program': True, 'referral_formset': ReferralPerkFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'challengecontent' in model_name: context.update({'is_challenge_section': True, 'challenge_formset': ChallengeProblemFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'solutioncontent' in model_name: context.update({'is_solution_section': True, 'solution_formset': SolutionFeatureFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'uspcontent' in model_name: context.update({'is_usp_section': True, 'usp_formset': USPContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'howitworkscontent' in model_name: context.update({'is_hiw_section': True, 'hiw_formset': HIWStepFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'whoisthisforcontent' in model_name: context.update({'is_who_section': True, 'who_formset': StoreTypeContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'testimonialcontent' in model_name: context.update({'is_testimonial_section': True, 'testimonial_formset': TestimonialContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'comparisoncontent' in model_name: context.update({'is_comparison_section': True, 'comparison_formset': ComparisonContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'faqcontent' in model_name: context.update({'is_faq_section': True, 'faq_formset': FAQContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'trustcontent' in model_name: context.update({'is_trust_section': True, 'trust_formset': TrustContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'pricingcontent' in model_name: context.update({'is_pricing_section': True, 'pricing_formset': PricingFeatureFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'landingpagecontent' in model_name:
            context.update({'is_landing_page': True})
            if self.request.GET.get('master') == '1':
                context.update({
                    'is_master_editor': True,
                    'is_challenge_section': True, 'challenge_formset': ChallengeProblemFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_solution_section': True, 'solution_formset': SolutionFeatureFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_usp_section': True, 'usp_formset': USPContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_hiw_section': True, 'hiw_formset': HIWStepFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_who_section': True, 'who_formset': StoreTypeContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_pricing_section': True, 'pricing_formset': PricingFeatureFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_referral_program': True, 'referral_formset': ReferralPerkFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_testimonial_section': True, 'testimonial_formset': TestimonialContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_comparison_section': True, 'comparison_formset': ComparisonContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_faq_section': True, 'faq_formset': FAQContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                    'is_trust_section': True, 'trust_formset': TrustContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                })
        elif 'policy' in model_name: 
            context.update({
                'is_policy': True, 
                'section_formset': PolicySectionFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object),
                'is_viewing_policy': True
            })
        elif 'footer' in model_name: context.update({'is_footer_page': True, 'social_formset': SocialLinkFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        
        scheme, host = self.request.scheme, self.request.get_host()
        base_url = f"{scheme}://{host}"
        # Consolidated Preview URL Logic
        if 'policy' in model_name:
            context['preview_url'] = f"{base_url}/policy/{self.object.slug}?is_preview=1"
        elif model_name in ['aboutpagecontent', 'aboutherocontent', 'aboutstorycontent', 'aboutmissioncontent', 'aboutwhychoosecontent', 'aboutservecontent', 'aboutctacontent']:
            context['preview_url'] = f"{base_url}/about?is_preview=1"
            if section and section != 'all':
                context['preview_url'] += f"&section={section}"
                # Adding scroll_target bindings for About Us
                if section == 'hero': context['scroll_target'] = 'hero'
                elif section == 'story': context['scroll_target'] = 'about'
                elif section == 'mission': context['scroll_target'] = 'mission'
                elif section == 'why': context['scroll_target'] = 'why_choose'
                elif section == 'serve': context['scroll_target'] = 'serve'
                elif section == 'cta': context['scroll_target'] = 'cta'
        elif 'landingpagecontent' in model_name: 
            context['preview_url'] = f"{base_url}/?is_preview=1"
            if context['section_param']:
                context['preview_url'] += f"&section={context['section_param']}"
                context['scroll_target'] = context['section_param']
            elif not context.get('is_master_editor'):
                context['preview_url'] += "&section=hero"
                context['scroll_target'] = 'hero'
        elif 'contactpagecontent' in model_name:
            context['preview_url'] = f"{base_url}/contact?is_preview=1"
            if context['section_param']:
                context['preview_url'] += f"&section={context['section_param']}"
                context['scroll_target'] = context['section_param']
            else:
                context['scroll_target'] = 'hero'
        elif model_name == 'ctacontent': context.update({'preview_url': f"{base_url}/?is_preview=1&section=cta", 'scroll_target': 'cta'})
        elif 'trustcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=trusted-retailers", 'scroll_target': 'trusted-retailers'})
        elif 'referralprogramcontent' in model_name: context.update({'preview_url': f"{base_url}/referral?is_preview=1", 'scroll_target': 'referral'})
        elif 'challengecontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=problem", 'scroll_target': 'problem'})
        elif 'solutioncontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=solution", 'scroll_target': 'solution'})
        elif 'uspcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=usp", 'scroll_target': 'usp'})
        elif 'howitworkscontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=how-it-works", 'scroll_target': 'how-it-works'})
        elif 'whoisthisforcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=who-is-this-for", 'scroll_target': 'who-is-this-for'})
        elif 'testimonialcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=testimonials", 'scroll_target': 'testimonials'})
        elif 'comparisoncontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=comparison", 'scroll_target': 'comparison'})
        elif 'faqcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=faq", 'scroll_target': 'faq'})
        elif 'pricingcontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=pricing", 'scroll_target': 'pricing'})
        elif model_name in ['careerpage', 'careerherocontent', 'careerculturecontent', 'careerperkscontent', 'careerjobscontent', 'careerctacontent']:
            context['preview_url'] = f"{base_url}/career?is_preview=1"
            if section and section != 'all': context['preview_url'] += f"&section={section}"
        elif 'childjobposition' in model_name: context.update({'preview_url': f"{base_url}/career/{self.object.slug}?is_preview=1"})
        elif 'footer' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=footer", 'scroll_target': 'master-footer'})
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        model_name = self.kwargs.get('model_name', '').lower()
        formset_keys = {
            'careerpage': ['culture_formset', 'perk_formset', 'job_formset'],
            'careerculturecontent': ['culture_formset'],
            'careerperkscontent': ['perk_formset'],
            'careerjobscontent': ['job_formset'],
            'childjobposition': ['description_formset', 'skill_formset'],
            'aboutpagecontent': ['serve_formset', 'why_formset'],
            'aboutwhychoosecontent': ['why_formset'],
            'aboutservecontent': ['serve_formset'],
            'referralprogramcontent': ['referral_formset'],
            'challengecontent': ['challenge_formset'],
            'solutioncontent': ['solution_formset'],
            'uspcontent': ['usp_formset'],
            'howitworkscontent': ['hiw_formset'],
            'whoisthisforcontent': ['who_formset'],
            'testimonialcontent': ['testimonial_formset'],
            'comparisoncontent': ['comparison_formset'],
            'faqcontent': ['faq_formset'],
            'trustcontent': ['trust_formset'],
            'pricingcontent': ['pricing_formset'],
            'landingpagecontent': ['challenge_formset', 'solution_formset', 'usp_formset', 'hiw_formset', 'who_formset', 'pricing_formset', 'referral_formset', 'testimonial_formset', 'comparison_formset', 'faq_formset', 'trust_formset'],
            'policy': ['section_formset'],
            'footer': ['social_formset'],
        }
        if model_name in formset_keys:
            formsets = [context[k] for k in formset_keys[model_name] if k in context]
            if all(fs.is_valid() for fs in formsets):
                self.object = form.save()
                for fs in formsets: fs.instance = self.object; fs.save()
                return super().form_valid(form)
            else: return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('custom_admin:model_list', kwargs={'app_label': self.kwargs.get('app_label', 'website'), 'model_name': self.kwargs.get('model_name')})

class CustomAdminDeleteView(AdminRequiredMixin, DynamicModelMixin, DeleteView):
    template_name = 'custom_admin/model_confirm_delete.html'
    def get_success_url(self):
        return reverse('custom_admin:model_list', kwargs={'app_label': self.kwargs.get('app_label', 'website'), 'model_name': self.kwargs.get('model_name')})

class ManageAllStoreTypesView(AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/model_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Demo Form Store Types'
        context['model_name_plural'] = 'Store Types'
        context['app_label'] = 'website'
        context['model_slug'] = 'allstoretype'
        context['model_class_name'] = 'AllStoreType'
        context['is_allstoretype_section'] = True
        context['is_manage_view'] = True
        context['allstoretype_formset'] = AllStoreTypeFormSet(
            self.request.POST or None, 
            queryset=AllStoreType.objects.all().order_by('id')
        )
        context['cancel_url'] = reverse('custom_admin:dashboard')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        formset = context['allstoretype_formset']
        if formset.is_valid():
            formset.save()
            return redirect('custom_admin:manage_allstoretype')
        return self.render_to_response(context)


def json_response(data, status=200):
   return HttpResponse(json.dumps(data), content_type="application/json", status=status)
