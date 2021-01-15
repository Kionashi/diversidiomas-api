"""Contact Urls"""

# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from contact.views import newsletter as newsletter_views

router = DefaultRouter(trailing_slash=False)
router.register(r'newsletter', newsletter_views.NewsletterViewset, basename='newsletter')

urlpatterns = [ 
    path('', include(router.urls)),
    
]