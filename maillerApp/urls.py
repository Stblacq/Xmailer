
from django.contrib import admin
from django.urls import path ,include
from core import views as vcore
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', vcore.home, name='home'),
    path('register', vcore.register, name='register'),
    path('dashboard', vcore.dashboard, name='dashboard'),
    path('froala_image', vcore.froala, name='froala'),
    path('dashboard/send_email', vcore.send_email, name='send_email'),
    path('dashboard/edit/<int:id>', vcore.edit_contact, name='edit_contact'),
    path('dashboard/delete/<int:id>', vcore.delete_contact, name='delete_contact'),
    path('dashboard/contacts', vcore.contacts, name='contacts'),
    path('account/password_change/done/', vcore.password_change_success, name='password_change_done'),
    path('admin/', admin.site.urls),
    path('account/', include('django.contrib.auth.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('core/media', document_root=settings.MEDIA_ROOT)