import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
django.setup()

from website.models import BlogPost

def seed_blog_images():
    # Images available in media/blogs/
    images = ['blog1.jpeg', 'blog4.jpg', 'blog6.png']
    
    posts = BlogPost.objects.all()
    print(f"Found {len(posts)} blog posts.")
    
    for i, post in enumerate(posts):
        # Rotate through the 3 images
        image_name = images[i % len(images)]
        post.featured_image = f"blogs/{image_name}"
        post.save()
        print(f"Updated post: {post.title} with image: {image_name}")

if __name__ == "__main__":
    seed_blog_images()
