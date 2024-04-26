from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

from blog import views

handler404 = 'core.views.page_not_found_view'
handler500 = 'core.views.server_error'


urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', views.RegistrCreateView.as_view(),
         name='registration'),
    path('profile/', include('users.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'АДМИНКА!!!'
admin.site.index_title = ' Решаем вопросики, на сайте!!! '
