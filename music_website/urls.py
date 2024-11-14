from django.urls import path
from music import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # User authentication and registration
    path('logout/', views.logout_view, name='logout'), 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # Home page and Admin dashboard
    path('', views.home, name='home'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),

    # Edit and Delete Song
    path('admin/song/edit/<int:song_id>/', views.edit_song, name='edit_song'),
    path('admin/song/delete/<int:song_id>/', views.delete_song, name='delete_song'),
    path('update_user_details/', views.update_user_details, name='update_user_details'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
