from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path("logout/", views.logoutView, name="logout"),
    path('home/<slug:slug>', views.DetailedBookView.as_view(), name='read'),
    path('add', views.CreateBookView, name='create'),
    path('admin-view', login_required(views.AdminView.as_view()), name='admin_view'),
    path('member-view', login_required(views.MemberView.as_view()), name='member_view'),
    path('edit/<int:id>', views.editBook, name='update'),
    path('delete/<int:id>', views.deleteBook, name='delete')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
