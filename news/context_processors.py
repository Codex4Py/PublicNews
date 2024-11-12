# context_processors.py
from .models import SocialMediaLink
from .models import Category


def social_media_links(request):
    links = SocialMediaLink.objects.all()  # Query to get all the social media links
    return {'social_media_links': links}
