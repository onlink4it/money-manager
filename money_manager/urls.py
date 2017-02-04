from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'money_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$',include('basic.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^basic/', include('basic.urls')),
    url(r'^invoices/', include('invoices.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)