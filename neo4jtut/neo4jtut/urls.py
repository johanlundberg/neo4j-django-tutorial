from django.conf.urls import include, url

# Static files for development
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'neo4jtut.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('neo4japp.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Static files for development
