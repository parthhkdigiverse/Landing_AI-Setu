from rest_framework import serializers
from .models import FAQ, AllStoreType, CareerPage, ChildJobPosition, ComparisonFeature, ContactPageContent, Culture, DemoVideo, JobDescription, JobPosition, JobSkill, LoginLink, Page, Perk, Policy, PolicySection, PricingSignup,DemoRequest, LandingPageContent, ContactSubmission, JobApplication, ReferralUser, BlogCategory, BlogPost, Section, SectionItem

# ... rest of file until the end ...

class BlogCategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    category = serializers.CharField(source='category.id', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class DemoRequestSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = DemoRequest
        fields = '__all__'

class PricingSignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = PricingSignup
        fields = '__all__'

class LandingPageContentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = LandingPageContent
        fields = '__all__'

class ContactSubmissionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = ContactSubmission
        fields = "__all__"

class JobApplicationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = JobApplication
        fields = "__all__"

class ReferralUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = ReferralUser
        fields = "__all__"

# class AboutPageSerializer(serializers.ModelSerializer):
#     # This line converts the MongoDB ObjectId into a string
#     id = serializers.CharField(read_only=True)

#     class Meta:
#         model = AboutPageContent
#         fields = '__all__' # Or list your specific fields

# class CareerPageSerializer(serializers.ModelSerializer):
#     # This MUST be CharField to handle MongoDB's string-based IDs
#     id = serializers.CharField(read_only=True)

#     class Meta:
#         model = CareerPageContent
#         fields = '__all__'

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

class LoginLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLink
        fields = "__all__"


class DemoVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoVideo
        fields = "__all__"

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return ObjectId(data)

class AllStoreTypeSerializer(serializers.ModelSerializer):
    id = ObjectIdField()    
    
    class Meta:
        model = AllStoreType
        fields = ["id", "name"]

class CultureSerializer(serializers.ModelSerializer):
    id = ObjectIdField()

    class Meta:
        model = Culture
        fields = "__all__"


class PerkSerializer(serializers.ModelSerializer):
    id = ObjectIdField()

    class Meta:
        model = Perk
        fields = "__all__"


class JobPositionSerializer(serializers.ModelSerializer):
    id = ObjectIdField()

    class Meta:
        model = JobPosition
        fields = "__all__"


class CareerPageSerializer(serializers.ModelSerializer):

    id = ObjectIdField()
    cultures = CultureSerializer(many=True)
    perks = PerkSerializer(many=True)
    jobs = JobPositionSerializer(many=True)

    class Meta:
        model = CareerPage
        fields = "__all__"

class JobDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobDescription
        fields = ["text"]


class JobSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobSkill
        fields = ["name"]


class ChildJobPositionSerializer(serializers.ModelSerializer):

    descriptions = JobDescriptionSerializer(many=True)
    skills = JobSkillSerializer(many=True)

    class Meta:
        model = ChildJobPosition
        fields = [
            "title",
            "slug",
            "location",
            "experience",
            "descriptions",
            "skills"
        ]

# class ObjectIdField(serializers.Field):
#     def to_representation(self, value):
#         return str(value)


class SectionItemSerializer(serializers.ModelSerializer):
    id = ObjectIdField()
    section = ObjectIdField()  # ✅ FIX FK

    class Meta:
        model = SectionItem
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    id = ObjectIdField()
    page = ObjectIdField()     # ✅ FIX FK
    items = SectionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    id = ObjectIdField()
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = "__all__"

class PolicySectionSerializer(serializers.ModelSerializer):
    id = serializers.CharField() 

    class Meta:
        model = PolicySection
        fields = ["id", "heading", "content", "order"]


class PolicySerializer(serializers.ModelSerializer):
    id = serializers.CharField()   
    sections = PolicySectionSerializer(many=True, read_only=True)

    class Meta:
        model = Policy
        fields = ["id", "title", "slug", "description", "sections"]