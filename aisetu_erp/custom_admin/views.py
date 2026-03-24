from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random, string, json
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.apps import apps
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from functools import wraps

from django.forms import inlineformset_factory
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
    HeroContent, AboutPageContent, AboutUsServeItem, Policy, PolicySection
)
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
OpenPositionFormSet = inlineformset_factory(CareerPage, JobPosition, fk_name='career_page', fields='__all__', extra=1, can_delete=True)
JobDescriptionFormSet = inlineformset_factory(ChildJobPosition, JobDescription, fk_name='job', fields='__all__', extra=1, can_delete=True)
JobSkillFormSet = inlineformset_factory(ChildJobPosition, JobSkill, fk_name='job', fields='__all__', extra=1, can_delete=True)

# About & Policy Formsets
ServeItemFormSet = inlineformset_factory(AboutPageContent, AboutUsServeItem, fk_name='about_page', fields='__all__', extra=1, can_delete=True)
PolicySectionFormSet = inlineformset_factory(Policy, PolicySection, fk_name='policy', fields='__all__', extra=1, can_delete=True)

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
        
        elif 'storetype' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=who-is-this-for", 'scroll_target': 'who-is-this-for'})
        
        readonly_models = ['demorequest', 'jobapplication', 'pricingsignup', 'contactsubmission', 'payment']
        context['is_readonly'] = model_name in readonly_models
        if context['is_readonly']:
            context['headers'] = [f.verbose_name.title() for f in context.get('fields', [])]
            rows = []
            for obj in context.get('object_list', []):
                row_data = []
                for f in context.get('fields', []):
                    val = getattr(obj, f.name, '')
                    if val and hasattr(val, 'url'):
                        val = f"<a href='javascript:void(0)' data-file-url='{val.url}' class='view-file-btn text-decoration-none'><i class='bi bi-file-earmark-text'></i> View</a>"
                    else: val = str(val) if val is not None else ''
                    row_data.append(val)
                rows.append({'pk': obj.pk, 'data': row_data})
            context['tabular_rows'] = rows
        return context

class CustomAdminCreateView(AdminRequiredMixin, DynamicModelMixin, CreateView):
    template_name = 'custom_admin/model_form.html'
    def get_form_class(self):
        from django.forms import modelform_factory
        model, model_name = self.get_model(), self.kwargs.get('model_name', '').lower()
        hero_fields = ['hero_eyebrow', 'hero_title', 'hero_highlighted_title', 'hero_subtitle', 'hero_highlights', 'primary_cta_text', 'secondary_cta_text', 'trusted_retailers_count', 'hero_stats_label', 'hero_stats_value']
        cta_fields = ['cta_badge', 'cta_title', 'cta_description', 'cta_button_text', 'cta_small_text']
        seo_fields = ['seo_title', 'seo_description', 'seo_keywords']
        
        if model_name == 'pricingcontent':
            fields = ['pricing_main_title', 'pricing_main_desc', 'pricing_label', 'pricing_title', 'pricing_plan_name', 'pricing_old_price', 'pricing_price', 'pricing_price_suffix']
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
        if 'careerpage' in model_name: context.update({'is_career_page': True, 'culture_formset': CultureFormSet(self.request.POST or None, self.request.FILES or None), 'perk_formset': PerkFormSet(self.request.POST or None, self.request.FILES or None), 'job_formset': OpenPositionFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'childjobposition' in model_name: context.update({'is_child_job_position': True, 'description_formset': JobDescriptionFormSet(self.request.POST or None, self.request.FILES or None), 'skill_formset': JobSkillFormSet(self.request.POST or None, self.request.FILES or None)})
        elif 'aboutpagecontent' in model_name: context.update({'is_about_page': True, 'serve_formset': ServeItemFormSet(self.request.POST or None, self.request.FILES or None)})
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
        if 'aboutpagecontent' in model_name: context['preview_url'] = f"{base_url}/about"
        elif 'landingpagecontent' in model_name: context['preview_url'] = f"{base_url}/?is_preview=1"
        elif 'ctacontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=cta", 'scroll_target': 'cta'})
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
        elif 'careerpage' in model_name: context['preview_url'] = f"{base_url}/career"
        elif 'contactpagecontent' in model_name: context['preview_url'] = f"{base_url}/contact"
        elif 'childjobposition' in model_name: context.update({'preview_url': f"{base_url}/career/?is_preview=1&section=open_positions", 'scroll_target': 'open_positions'})
        elif 'policy' == model_name: context['preview_url'] = f"{base_url}/policy/new-policy"
        elif 'blogpost' in model_name: context['preview_url'] = f"{base_url}/blog"
        elif 'footer' == model_name: context['preview_url'] = f"{base_url}/"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        model_name = self.kwargs.get('model_name', '').lower()
        formset_keys = {
            'careerpage': ['culture_formset', 'perk_formset', 'job_formset'],
            'childjobposition': ['description_formset', 'skill_formset'],
            'aboutpagecontent': ['serve_formset'],
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
        }
        if model_name in formset_keys:
            formsets = [context[k] for k in formset_keys[model_name]]
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
        seo_fields = ['seo_title', 'seo_description', 'seo_keywords']
        
        # Landing Page Sub-sections (Model fields from LandingPageContent)
        trust_fields = ['trust_item1', 'trust_item2', 'trust_item3', 'trust_item4']
        challenge_fields = ['problem_section_label', 'problem_section_title']
        solution_fields = ['feature_title', 'feature_title2', 'solution_section_label', 'solution_section_title']
        usp_fields = ['usp_badge_text', 'usp_title', 'usp_description']
        hiw_fields = ['howitworks_label', 'howitworks_title']
        who_fields = ['who_main_title', 'who_title']
        pricing_fields = ['pricing_main_title', 'pricing_main_desc', 'pricing_label', 'pricing_title', 'pricing_plan_name', 'pricing_old_price', 'pricing_price', 'pricing_price_suffix'] + [f'pricing_feature{i}' for i in range(1, 9)]
        referral_fields = ['referral_main_title', 'referral_main_desc', 'referral_label', 'referral_title', 'join_referral']
        testimonial_fields = ['testimonial_label', 'testimonial_title', 'review_button', 'all_reviews_title', 'all_reviews_desc']
        comparison_fields = ['comparison_title', 'comparison_subtitle', 'comparison_title1', 'comparison_title2', 'comparison_title3']
        faq_fields = ['faq_label', 'faq_title']
        cta_fields = ['cta_badge', 'cta_title', 'cta_description', 'cta_button_text', 'cta_small_text']

        # Contact Page Sub-sections
        contact_hero = ['hero_title', 'hero_description']
        contact_cards = ['call_title', 'call_phone', 'call_phone_number', 'call_subtext', 'email_title', 'email_address', 'email_address_link', 'email_subtext', 'visit_title', 'visit_address', 'visit_subtext', 'visit_map_url', 'support_title', 'support_time', 'support_subtext']
        contact_form = ['form_title', 'name_label', 'name_placeholder', 'phone_label', 'phone_placeholder', 'email_label', 'email_placeholder', 'company_label', 'company_placeholder', 'message_label', 'message_placeholder', 'form_button_text']
        contact_why = ['why_title', 'why_description', 'feature_1_title', 'feature_2_title', 'feature_3_title', 'feature_4_title']
        contact_cta = ['cta_title', 'cta_description', 'cta_button_text1', 'cta_button_text2', 'cta_button_text3']

        # About Page Sub-sections
        about_hero = ['hero_title', 'hero_subtitle']
        about_content = ['about_label', 'about_heading', 'about_image', 'about_description_1', 'about_description_2', 'about_description_3']
        about_mission = ['mission_title', 'mission_description']
        about_why = ['why_choose_title', 'why_point_1', 'why_point_2', 'why_point_3', 'why_point_4', 'why_point_5']
        about_serve = ['serve_title', 'serve_subtitle']
        about_cta = ['cta_title', 'cta_description', 'cta_button_text']

        # --- Model Routing ---
        if model_name == 'landingpagecontent':
            if section == 'hero': fields = hero_fields
            elif section == 'seo': fields = seo_fields
            else: fields = hero_fields + seo_fields
        elif model_name == 'herocontent': fields = hero_fields
        elif model_name == 'trustcontent': fields = trust_fields
        elif model_name == 'challengecontent': fields = challenge_fields
        elif model_name == 'solutioncontent': fields = solution_fields
        elif model_name == 'uspcontent': fields = usp_fields
        elif model_name == 'howitworkscontent': fields = hiw_fields
        elif model_name == 'whoisthisforcontent': fields = who_fields
        elif model_name == 'pricingcontent': fields = pricing_fields
        elif model_name == 'referralprogramcontent': fields = referral_fields
        elif model_name == 'testimonialcontent': fields = testimonial_fields
        elif model_name == 'comparisoncontent': fields = comparison_fields
        elif model_name == 'faqcontent': fields = faq_fields
        elif model_name == 'ctacontent': fields = cta_fields
        
        elif model_name == 'contactpagecontent':
            if section == 'hero': fields = contact_hero
            elif section == 'contact_cards': fields = contact_cards
            elif section == 'form': fields = contact_form
            elif section == 'why_choose': fields = contact_why
            elif section == 'cta': fields = contact_cta
            elif section == 'seo': fields = seo_fields
            else: fields = contact_hero + contact_cards + contact_form + contact_why + contact_cta + seo_fields
            
        elif model_name == 'aboutpagecontent':
            if section == 'hero': fields = about_hero
            elif section == 'content': fields = about_content
            elif section == 'mission': fields = about_mission
            elif section == 'why_choose': fields = about_why
            elif section == 'serve': fields = about_serve
            elif section == 'cta': fields = about_cta
            else: fields = about_hero + about_content + about_mission + about_why + about_serve + about_cta
        
        else: fields = '__all__'
        
        return modelform_factory(model, fields=fields)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.request.GET.get('section')
        context['section_param'] = section
        model_name = self.kwargs.get('model_name', '').lower().strip()
        
        # --- Resolve Dynamic Section Title ---
        if section:
            titles = {
                'hero': 'Hero Section', 'trust_strip': 'Trust Strip', 'problem': 'The Challenge',
                'solution': 'Solutions', 'usp': 'USP Features', 'how_it_works': 'How It Works',
                'who_is_this_for': 'Who Is This For', 'pricing': 'Pricing Plan', 'referral': 'Referral Perks',
                'comparison': 'Comparisons', 'testimonials': 'Testimonials', 'faq': 'FAQs', 'cta': 'Final CTA',
                'contact_cards': 'Contact Cards', 'form': 'Contact Form', 'why_choose': 'Why Choose Us', 'seo': 'SEO Metadata',
                'content': 'About Details', 'mission': 'Our Mission', 'serve': 'Who We Serve'
            }
            context['section_title'] = titles.get(section, section.replace('_', ' ').title())
        
        if 'careerpage' in model_name: context.update({'is_career_page': True, 'culture_formset': CultureFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object), 'perk_formset': PerkFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object), 'job_formset': OpenPositionFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'childjobposition' in model_name: context.update({'is_child_job_position': True, 'description_formset': JobDescriptionFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object), 'skill_formset': JobSkillFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'aboutpagecontent' in model_name:
            context.update({'is_about_page': True})
            if not section or section == 'serve':
                context.update({'serve_formset': ServeItemFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
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
        elif 'policy' == model_name: context.update({'is_policy': True, 'section_formset': PolicySectionFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        
        scheme, host = self.request.scheme, self.request.get_host()
        base_url = f"{scheme}://{host}"
        
        if 'aboutpagecontent' in model_name: 
            context['preview_url'] = f"{base_url}/about"
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
        elif 'ctacontent' in model_name: context.update({'preview_url': f"{base_url}/?is_preview=1&section=cta", 'scroll_target': 'cta'})
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
        elif 'careerpage' in model_name: context['preview_url'] = f"{base_url}/career"
        elif 'childjobposition' in model_name: context['preview_url'] = f"{base_url}/career/{self.object.slug}"
        elif 'policy' == model_name: context['preview_url'] = f"{base_url}/policy/new-policy"
        elif 'blogpost' in model_name: context['preview_url'] = f"{base_url}/blog"
        elif 'footer' == model_name: context['preview_url'] = f"{base_url}/"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        model_name = self.kwargs.get('model_name', '').lower()
        formset_keys = {
            'careerpage': ['culture_formset', 'perk_formset', 'job_formset'],
            'childjobposition': ['description_formset', 'skill_formset'],
            'aboutpagecontent': ['serve_formset'],
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
        }
        if model_name in formset_keys:
            formsets = [context[k] for k in formset_keys[model_name]]
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
        return reverse('custom_admin:model_list', kwargs={'app_label': self.kwargs.get('app_label', 'website'), 'model_name': self.kwargs.get('model_slug')})

@custom_admin_required
def page_sections(request, page_type='landing'):
    if page_type == 'landing':
        content = LandingPageContent.objects.first()
        if not content: content = LandingPageContent.objects.create()
        title = "Landing Page Sections"
        sections = [
            {'id': 'hero', 'name': 'Hero Section', 'toggle_field': 'show_hero', 'is_visible': content.show_hero, 'icon': 'bi-app-indicator', 'edit_url': reverse('custom_admin:edit_singleton', args=['landingpagecontent']) + '?section=hero'},
            {'id': 'trust_strip', 'name': 'Trust Strip', 'toggle_field': 'show_trust_strip', 'is_visible': content.show_trust_strip, 'icon': 'bi-shield-check', 'edit_url': reverse('custom_admin:edit_singleton', args=['trustcontent'])},
            {'id': 'problem', 'name': 'The Challenge', 'toggle_field': 'show_problem', 'is_visible': content.show_problem, 'icon': 'bi-exclamation-square', 'edit_url': reverse('custom_admin:edit_singleton', args=['challengecontent'])},
            {'id': 'solution', 'name': 'Solutions', 'toggle_field': 'show_solution', 'is_visible': content.show_solution, 'icon': 'bi-lightbulb', 'edit_url': reverse('custom_admin:edit_singleton', args=['solutioncontent'])},
            {'id': 'usp', 'name': 'USP Features', 'toggle_field': 'show_usp', 'is_visible': content.show_usp, 'icon': 'bi-stars', 'edit_url': reverse('custom_admin:edit_singleton', args=['uspcontent'])},
            {'id': 'how_it_works', 'name': 'How It Works', 'toggle_field': 'show_how_it_works', 'is_visible': content.show_how_it_works, 'icon': 'bi-diagram-3', 'edit_url': reverse('custom_admin:edit_singleton', args=['howitworkscontent'])},
            {'id': 'who_is_this_for', 'name': 'Who Is This For', 'toggle_field': 'show_who_is_this_for', 'is_visible': content.show_who_is_this_for, 'icon': 'bi-people-fill', 'edit_url': reverse('custom_admin:edit_singleton', args=['whoisthisforcontent'])},
            {'id': 'pricing', 'name': 'Pricing Plan', 'toggle_field': 'show_pricing', 'is_visible': content.show_pricing, 'icon': 'bi-tags', 'edit_url': reverse('custom_admin:edit_singleton', args=['pricingcontent'])},
            {'id': 'referral', 'name': 'Referral Perks', 'toggle_field': 'show_referral', 'is_visible': content.show_referral, 'icon': 'bi-gift-fill', 'edit_url': reverse('custom_admin:edit_singleton', args=['referralprogramcontent'])},
            {'id': 'comparison', 'name': 'Comparisons', 'toggle_field': 'show_comparison', 'is_visible': content.show_comparison, 'icon': 'bi-layers-half', 'edit_url': reverse('custom_admin:edit_singleton', args=['comparisoncontent'])},
            {'id': 'testimonials', 'name': 'Testimonials', 'toggle_field': 'show_testimonials', 'is_visible': content.show_testimonials, 'icon': 'bi-chat-square-quote', 'edit_url': reverse('custom_admin:edit_singleton', args=['testimonialcontent'])},
            {'id': 'faq', 'name': 'FAQs', 'toggle_field': 'show_faq', 'is_visible': content.show_faq, 'icon': 'bi-question-diamond', 'edit_url': reverse('custom_admin:edit_singleton', args=['faqcontent'])},
            {'id': 'cta', 'name': 'Final CTA', 'toggle_field': 'show_cta', 'is_visible': content.show_cta, 'icon': 'bi-bullseye', 'edit_url': reverse('custom_admin:edit_singleton', args=['ctacontent'])},
        ]
    else: # contact
        content = ContactPageContent.objects.first()
        if not content: content = ContactPageContent.objects.create()
        title = "Contact Page Sections"
        sections = [
            {'id': 'hero', 'name': 'Hero Section', 'toggle_field': 'show_hero', 'is_visible': content.show_hero, 'icon': 'bi-app-indicator', 'edit_url': reverse('custom_admin:edit_singleton', args=['contactpagecontent']) + '?section=hero'},
            {'id': 'contact_cards', 'name': 'Contact Cards', 'toggle_field': 'show_cards', 'is_visible': content.show_cards, 'icon': 'bi-card-list', 'edit_url': reverse('custom_admin:edit_singleton', args=['contactpagecontent']) + '?section=contact_cards'},
            {'id': 'form', 'name': 'Contact Form', 'toggle_field': 'show_form', 'is_visible': content.show_form, 'icon': 'bi-envelope-paper', 'edit_url': reverse('custom_admin:edit_singleton', args=['contactpagecontent']) + '?section=form'},
            {'id': 'why_choose', 'name': 'Why Choose Us', 'toggle_field': 'show_why_choose', 'is_visible': content.show_why_choose, 'icon': 'bi-patch-check', 'edit_url': reverse('custom_admin:edit_singleton', args=['contactpagecontent']) + '?section=why_choose'},
            {'id': 'cta', 'name': 'Final CTA', 'toggle_field': 'show_cta', 'is_visible': content.show_cta, 'icon': 'bi-bullseye', 'edit_url': reverse('custom_admin:edit_singleton', args=['contactpagecontent']) + '?section=cta'},
        ]
    
    return render(request, 'custom_admin/page_sections.html', {
        'sections': sections,

        'page_title': title,
        'page_type': page_type
    })

@csrf_exempt
@custom_admin_required
def toggle_section_visibility(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        page_type = data.get('page_type', 'landing')
        field_name = data.get('field_name')
        is_visible = data.get('is_visible')
        
        Model = LandingPageContent if page_type == 'landing' else ContactPageContent
        content = Model.objects.first()
        if content and hasattr(content, field_name):
            setattr(content, field_name, is_visible)
            content.save()
            return json_response({'status': 'success'})
    return json_response({'status': 'error'}, status=400)

def json_response(data, status=200):
   return HttpResponse(json.dumps(data), content_type="application/json", status=status)
