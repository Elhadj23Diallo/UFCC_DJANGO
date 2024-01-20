from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path
from django.urls.conf import include
from blog.views import get_paypal_keys

urlpatterns = [
    path('admin/', admin.site.urls),
   path('', include('authentication.urls')),
   path('blog/', include('blog.urls')),
   path('', include('paypal.standard.ipn.urls')),
   path('get_paypal_keys/', get_paypal_keys, name='get_paypal_keys'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
