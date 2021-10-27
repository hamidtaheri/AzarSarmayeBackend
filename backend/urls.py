from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
import api.urls
from django.conf.urls.static import static


urlpatterns = [
    # url('', auth_views.LoginView.as_view(), name='login'),
    # url('login/', auth_views.LoginView.as_view(), name='login'),
    # url('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('api/', include(api.urls)),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

