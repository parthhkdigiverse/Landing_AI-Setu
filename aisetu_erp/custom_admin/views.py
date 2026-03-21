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
from website.models import ChildJobPosition, JobDescription, JobSkill

# Career Formsets
CultureFormSet = inlineformset_factory(CareerPage, Culture, fields='__all__', extra=1, can_delete=True)
PerkFormSet = inlineformset_factory(CareerPage, Perk, fields='__all__', extra=1, can_delete=True)
OpenPositionFormSet = inlineformset_factory(CareerPage, JobPosition, fields='__all__', extra=1, can_delete=True)

# ChildJobPosition Formsets
JobDescriptionFormSet = inlineformset_factory(ChildJobPosition, JobDescription, fields='__all__', extra=1, can_delete=True)
JobSkillFormSet = inlineformset_factory(ChildJobPosition, JobSkill, fields='__all__', extra=1, can_delete=True)

# Policy Formsets
from website.models import Policy, PolicySection
PolicySectionFormSet = inlineformset_factory(Policy, PolicySection, fields='__all__', extra=1, can_delete=True)

# About Page Formsets
from website.models import AboutPageContent, AboutUsServeItem
ServeItemFormSet = inlineformset_factory(AboutPageContent, AboutUsServeItem, fields='__all__', extra=1, can_delete=True)

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
    context = {
        'demo_count': DemoRequest.objects.count(),
        'signup_count': PricingSignup.objects.count(),
        'payment_count': Payment.objects.count(),
        'contact_count': ContactSubmission.objects.count(),
    }
    return render(request, 'custom_admin/dashboard.html', context)

# --- Generic CRUD Views ---
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
        
        # Determine columns for list view
        if hasattr(self, 'object_list'):
            fields = [f for f in model._meta.fields if f.name not in ['id', '_id', 'password']]
            context['fields'] = fields[:5] # Show first 5 fields in table
        return context

class CustomAdminListView(AdminRequiredMixin, DynamicModelMixin, ListView):
    template_name = 'custom_admin/model_list.html'
    paginate_by = 20

class CustomAdminCreateView(AdminRequiredMixin, DynamicModelMixin, CreateView):
    template_name = 'custom_admin/model_form.html'
    
    def get_form_class(self):
        from django.forms import modelform_factory
        model = self.get_model()
        model_name = self.kwargs.get('model_name', '').lower()
        if model_name == 'pricingcontent':
            fields = ['pricing_main_title', 'pricing_main_desc', 'pricing_label', 'pricing_title', 'pricing_plan_name', 'pricing_old_price', 'pricing_price', 'pricing_price_suffix', 'pricing_feature1', 'pricing_feature2', 'pricing_feature3', 'pricing_feature4', 'pricing_feature5', 'pricing_feature6', 'pricing_feature7', 'pricing_feature8']
        elif model_name == 'landingpagecontent':
            fields = ['hero_eyebrow', 'hero_title', 'hero_highlighted_title', 'hero_subtitle', 'hero_highlights', 'primary_cta_text', 'secondary_cta_text', 'trusted_retailers_count', 'hero_stats_label', 'hero_stats_value', 'trust_item1', 'trust_item2', 'trust_item3', 'trust_item4', 'problem_section_label', 'problem_section_title', 'feature_title', 'feature_title2', 'solution_section_label', 'solution_section_title', 'usp_badge_text', 'usp_title', 'usp_description', 'howitworks_label', 'howitworks_title', 'who_main_title', 'who_title', 'referral_main_title', 'referral_main_desc', 'referral_label', 'referral_title', 'join_referral', 'comparison_title', 'comparison_subtitle', 'comparison_title1', 'comparison_title2', 'comparison_title3', 'testimonial_label', 'testimonial_title', 'review_button', 'all_reviews_title', 'all_reviews_desc', 'faq_label', 'faq_title', 'cta_badge', 'cta_title', 'cta_description', 'cta_button_text', 'cta_small_text', 'seo_title', 'seo_description', 'seo_keywords']
        else:
            fields = '__all__'
        return modelform_factory(model, fields=fields)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get('model_name', '').lower().strip()
        if 'careerpage' in model_name:
            context['is_career_page'] = True
            if self.request.method == 'POST':
                context['culture_formset'] = CultureFormSet(self.request.POST, self.request.FILES)
                context['perk_formset'] = PerkFormSet(self.request.POST, self.request.FILES)
                context['job_formset'] = OpenPositionFormSet(self.request.POST, self.request.FILES)
            else:
                context['culture_formset'] = CultureFormSet()
                context['perk_formset'] = PerkFormSet()
                context['job_formset'] = OpenPositionFormSet()
        elif 'childjobposition' in model_name:
            context['is_child_job_position'] = True
            if self.request.method == 'POST':
                context['description_formset'] = JobDescriptionFormSet(self.request.POST, self.request.FILES)
                context['skill_formset'] = JobSkillFormSet(self.request.POST, self.request.FILES)
            else:
                context['description_formset'] = JobDescriptionFormSet()
                context['skill_formset'] = JobSkillFormSet()
        elif 'aboutpagecontent' in model_name:
            context['is_about_page'] = True
            if self.request.method == 'POST':
                context['serve_formset'] = ServeItemFormSet(self.request.POST, self.request.FILES)
            else:
                context['serve_formset'] = ServeItemFormSet()

        elif 'policy' == model_name:
            context['is_policy'] = True
            if self.request.method == 'POST':
                context['section_formset'] = PolicySectionFormSet(self.request.POST, self.request.FILES)
            else:
                context['section_formset'] = PolicySectionFormSet()

        # Preview URL logic
        scheme = self.request.scheme
        host = self.request.get_host()
        base_url = f"{scheme}://{host}"
        
        if 'aboutpagecontent' in model_name:
            context['preview_url'] = f"{base_url}/about"
        elif 'landingpagecontent' in model_name:
            context['preview_url'] = f"{base_url}/"
        elif 'pricingcontent' in model_name:
            context['preview_url'] = f"{base_url}/pricing"
        elif 'careerpage' in model_name:
            context['preview_url'] = f"{base_url}/career"
        elif 'contactpagecontent' in model_name:
            context['preview_url'] = f"{base_url}/contact"
        elif 'childjobposition' in model_name:
            context['preview_url'] = f"{base_url}/career/new-job"
        elif 'policy' == model_name:
            context['preview_url'] = f"{base_url}/policy/new-policy"
        elif 'footer' == model_name:
            context['preview_url'] = f"{base_url}/"
            
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        model_name = self.kwargs.get('model_name', '').lower()
        
        if model_name == 'careerpage':
            culture_formset = context['culture_formset']
            perk_formset = context['perk_formset']
            job_formset = context['job_formset']
            
            if culture_formset.is_valid() and perk_formset.is_valid() and job_formset.is_valid():
                self.object = form.save()
                culture_formset.instance = self.object
                culture_formset.save()
                perk_formset.instance = self.object
                perk_formset.save()
                job_formset.instance = self.object
                job_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))
                
        elif model_name == 'childjobposition':
            description_formset = context['description_formset']
            skill_formset = context['skill_formset']
            
            if description_formset.is_valid() and skill_formset.is_valid():
                self.object = form.save()
                description_formset.instance = self.object
                description_formset.save()
                skill_formset.instance = self.object
                skill_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

        elif 'aboutpagecontent' in model_name:
            serve_formset = context['serve_formset']
            
            if serve_formset.is_valid():
                self.object = form.save()
                serve_formset.instance = self.object
                serve_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

        elif 'policy' == model_name:
            section_formset = context['section_formset']
            
            if section_formset.is_valid():
                self.object = form.save()
                section_formset.instance = self.object
                section_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))
                
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('custom_admin:model_list', kwargs={
            'app_label': self.kwargs.get('app_label', 'website'),
            'model_name': self.kwargs.get('model_name')
        })

class CustomAdminUpdateView(AdminRequiredMixin, DynamicModelMixin, UpdateView):
    template_name = 'custom_admin/model_form.html'
    
    def get_form_class(self):
        from django.forms import modelform_factory
        model = self.get_model()
        model_name = self.kwargs.get('model_name', '').lower()
        if model_name == 'pricingcontent':
            fields = ['pricing_main_title', 'pricing_main_desc', 'pricing_label', 'pricing_title', 'pricing_plan_name', 'pricing_old_price', 'pricing_price', 'pricing_price_suffix', 'pricing_feature1', 'pricing_feature2', 'pricing_feature3', 'pricing_feature4', 'pricing_feature5', 'pricing_feature6', 'pricing_feature7', 'pricing_feature8']
        elif model_name == 'landingpagecontent':
            fields = ['hero_eyebrow', 'hero_title', 'hero_highlighted_title', 'hero_subtitle', 'hero_highlights', 'primary_cta_text', 'secondary_cta_text', 'trusted_retailers_count', 'hero_stats_label', 'hero_stats_value', 'trust_item1', 'trust_item2', 'trust_item3', 'trust_item4', 'problem_section_label', 'problem_section_title', 'feature_title', 'feature_title2', 'solution_section_label', 'solution_section_title', 'usp_badge_text', 'usp_title', 'usp_description', 'howitworks_label', 'howitworks_title', 'who_main_title', 'who_title', 'referral_main_title', 'referral_main_desc', 'referral_label', 'referral_title', 'join_referral', 'comparison_title', 'comparison_subtitle', 'comparison_title1', 'comparison_title2', 'comparison_title3', 'testimonial_label', 'testimonial_title', 'review_button', 'all_reviews_title', 'all_reviews_desc', 'faq_label', 'faq_title', 'cta_badge', 'cta_title', 'cta_description', 'cta_button_text', 'cta_small_text', 'seo_title', 'seo_description', 'seo_keywords']
        else:
            fields = '__all__'
        return modelform_factory(model, fields=fields)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get('model_name', '').lower().strip()
        if 'careerpage' in model_name:
            context['is_career_page'] = True
            if self.request.method == 'POST':
                context['culture_formset'] = CultureFormSet(self.request.POST, self.request.FILES, instance=self.object)
                context['perk_formset'] = PerkFormSet(self.request.POST, self.request.FILES, instance=self.object)
                context['job_formset'] = OpenPositionFormSet(self.request.POST, self.request.FILES, instance=self.object)
            else:
                context['culture_formset'] = CultureFormSet(instance=self.object)
                context['perk_formset'] = PerkFormSet(instance=self.object)
                context['job_formset'] = OpenPositionFormSet(instance=self.object)
        elif 'childjobposition' in model_name:
            context['is_child_job_position'] = True
            if self.request.method == 'POST':
                context['description_formset'] = JobDescriptionFormSet(self.request.POST, self.request.FILES, instance=self.object)
                context['skill_formset'] = JobSkillFormSet(self.request.POST, self.request.FILES, instance=self.object)
            else:
                context['description_formset'] = JobDescriptionFormSet(instance=self.object)
                context['skill_formset'] = JobSkillFormSet(instance=self.object)
        elif 'aboutpagecontent' in model_name:
            context['is_about_page'] = True
            if self.request.method == 'POST':
                context['serve_formset'] = ServeItemFormSet(self.request.POST, self.request.FILES, instance=self.object)
            else:
                context['serve_formset'] = ServeItemFormSet(instance=self.object)

        elif 'policy' == model_name:
            context['is_policy'] = True
            if self.request.method == 'POST':
                context['section_formset'] = PolicySectionFormSet(self.request.POST, self.request.FILES, instance=self.object)
            else:
                context['section_formset'] = PolicySectionFormSet(instance=self.object)
                
        # Preview URL logic
        scheme = self.request.scheme
        host = self.request.get_host()
        base_url = f"{scheme}://{host}"
        
        if 'aboutpagecontent' in model_name:
            context['preview_url'] = f"{base_url}/about"
        elif 'landingpagecontent' in model_name:
            context['preview_url'] = f"{base_url}/"
        elif 'pricingcontent' in model_name:
            context['preview_url'] = f"{base_url}/pricing"
        elif 'careerpage' in model_name:
            context['preview_url'] = f"{base_url}/career"
        elif 'contactpagecontent' in model_name:
            context['preview_url'] = f"{base_url}/contact"
        elif 'childjobposition' in model_name:
            if hasattr(self, 'object') and self.object and getattr(self.object, 'slug', None):
                context['preview_url'] = f"{base_url}/career/{self.object.slug}"
            else:
                context['preview_url'] = f"{base_url}/career"
        elif 'policy' == model_name:
            if hasattr(self, 'object') and self.object and getattr(self.object, 'slug', None):
                context['preview_url'] = f"{base_url}/policy/{self.object.slug}"
            else:
                context['preview_url'] = f"{base_url}/policy/new-policy"
        elif 'footer' == model_name:
            context['preview_url'] = f"{base_url}/"
            
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        model_name = self.kwargs.get('model_name', '').lower()
        
        if model_name == 'careerpage':
            culture_formset = context['culture_formset']
            perk_formset = context['perk_formset']
            job_formset = context['job_formset']
            
            if culture_formset.is_valid() and perk_formset.is_valid() and job_formset.is_valid():
                self.object = form.save()
                culture_formset.instance = self.object
                culture_formset.save()
                perk_formset.instance = self.object
                perk_formset.save()
                job_formset.instance = self.object
                job_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))
                
        elif 'childjobposition' in model_name:
            description_formset = context['description_formset']
            skill_formset = context['skill_formset']
            
            if description_formset.is_valid() and skill_formset.is_valid():
                self.object = form.save()
                description_formset.instance = self.object
                description_formset.save()
                skill_formset.instance = self.object
                skill_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

        elif 'aboutpagecontent' in model_name:
            serve_formset = context['serve_formset']
            
            if serve_formset.is_valid():
                self.object = form.save()
                serve_formset.instance = self.object
                serve_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

        elif 'policy' == model_name:
            section_formset = context['section_formset']
            
            if section_formset.is_valid():
                self.object = form.save()
                section_formset.instance = self.object
                section_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))
                
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('custom_admin:model_list', kwargs={
            'app_label': self.kwargs.get('app_label', 'website'),
            'model_name': self.kwargs.get('model_name')
        })

class CustomAdminDeleteView(AdminRequiredMixin, DynamicModelMixin, DeleteView):
    template_name = 'custom_admin/model_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('custom_admin:model_list', kwargs={
            'app_label': self.kwargs.get('app_label', 'website'),
            'model_name': self.kwargs.get('model_name')
        })
