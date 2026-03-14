from rest_framework import serializers
from .models import FAQ, AboutPageContent, CareerPageContent, ComparisonFeature, ContactPageContent, PricingSignup,DemoRequest, LandingPageContent, ContactSubmission, JobApplication, ReferralUser


class DemoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoRequest
        fields = '__all__'

class PricingSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingSignup
        fields = '__all__'

class LandingPageContentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = LandingPageContent
        fields = '__all__'

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = "__all__"

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"

class ReferralUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralUser
        fields = "__all__"

class AboutPageSerializer(serializers.ModelSerializer):
    # This line converts the MongoDB ObjectId into a string
    id = serializers.CharField(read_only=True)

    class Meta:
        model = AboutPageContent
        fields = '__all__' # Or list your specific fields

class CareerPageSerializer(serializers.ModelSerializer):
    # This MUST be CharField to handle MongoDB's string-based IDs
    id = serializers.CharField(read_only=True)

    class Meta:
        model = CareerPageContent
        fields = '__all__'

class ContactPageContentSerializer(serializers.ModelSerializer):
    # This MUST be CharField to handle MongoDB's string-based IDs
    id = serializers.CharField(read_only=True)

    class Meta:
        model = ContactPageContent
        fields = '__all__'

class ComparisonFeatureSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()  # override id to string

    class Meta:
        model = ComparisonFeature
        fields = ['id', 'feature_name', 'has_ai_setu', 'has_traditional']

    def get_id(self, obj):
        return str(obj.id)
    
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'