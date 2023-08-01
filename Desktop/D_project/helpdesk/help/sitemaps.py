from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(selfself):
        return Post.published.all()

    def lastmod(selfself, obj):
        return obj.updated