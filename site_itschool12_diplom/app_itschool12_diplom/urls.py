from django.urls import path
from django.contrib.auth import views as auth_views
from django_registration.backends.one_step.views import RegistrationView
from . import views
from .forms import CustomRegistrationForm

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('accounts/register/',
         RegistrationView.as_view(
             form_class=CustomRegistrationForm,
             success_url='/',
             template_name='app_itschool12_diplom/register.html'), 
         name='django_registration_register'),
    path('courses/<int:course_pk>/lessons/<int:lesson_pk>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # ... другие URL-ы будут здесь
]