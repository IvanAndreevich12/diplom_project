from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_registration.backends.one_step.views import RegistrationView
from .models import Course, Lesson
from .forms import CustomRegistrationForm

def index(request):
    return render(request, 'app_itschool12_diplom/index.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'app_itschool12_diplom/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user_profile = request.user.profile if request.user.is_authenticated else None
    is_enrolled = course.students.filter(id=user_profile.id).exists() if user_profile else False
    return render(request, 'app_itschool12_diplom/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'user': request.user
    })

def lesson_detail(request, course_pk, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course__pk=course_pk)
    return render(request, 'app_itschool12_diplom/lesson_detail.html', {'lesson': lesson})

class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
    template_name = 'app_itschool12_diplom/register.html'
    success_url = '/'

class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    profile = request.user.profile
    course.students.add(profile)  # Добавляем студента на курс
    messages.success(request, 'Вы успешно записались на курс!')
    return redirect('course_detail', pk=pk)