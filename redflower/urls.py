from django.conf.urls import patterns, include, url
from django.contrib import admin
from oscar.app import application
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


from oscar.views import handler500, handler404, handler403  # noqa



admin.autodiscover()



urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'', include(application.urls)),
   
    url(r'^admin/', include(admin.site.urls)),
]



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



if settings.DEBUG:
    import debug_toolbar

    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        url(r'^403$', handler403),
        url(r'^404$', handler404),
        url(r'^500$', handler500),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]




