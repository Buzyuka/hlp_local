

from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from help.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('help/', include('help.urls', namespace='help')),
    path('sitemap.xml', sitemap,{'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]
