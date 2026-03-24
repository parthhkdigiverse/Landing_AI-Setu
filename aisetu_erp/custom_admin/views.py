import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
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
    ComparisonContent, FAQContent, HeroContent, CTAContent,
    AboutPageContent, AboutUsServeItem, Policy, PolicySection
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
    return redirect(reverse('custom_admin:model_update', kwargs={'app_label': 'website', 'model_name': model_name, 'pk': obj.pk}))

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
            context.update({
                'is_landing_page': True,
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
        elif 'childjobposition' in model_name: context['preview_url'] = f"{base_url}/career/new-job"
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
        if 'careerpage' in model_name: context.update({'is_career_page': True, 'culture_formset': CultureFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object), 'perk_formset': PerkFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object), 'job_formset': OpenPositionFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'childjobposition' in model_name: context.update({'is_child_job_position': True, 'description_formset': JobDescriptionFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object), 'skill_formset': JobSkillFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
        elif 'aboutpagecontent' in model_name: context.update({'is_about_page': True, 'serve_formset': ServeItemFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)})
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
            context.update({
                'is_landing_page': True,
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
        elif 'childjobposition' in model_name: context['preview_url'] = f"{base_url}/career/new-job"
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
