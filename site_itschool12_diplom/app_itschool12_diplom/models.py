from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.user.username}"

class Course(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    start_date = models.DateField("Дата начала", null=True, blank=True)
    end_date = models.DateField("Дата окончания", null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_taught', verbose_name="Преподаватель")
    students = models.ManyToManyField(Profile, related_name='courses_enrolled', blank=True, verbose_name="Студенты")

    def __str__(self):
        return f"{self.title} (ID: {self.id})"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Курс")
    title = models.CharField("Название", max_length=255)
    content = models.TextField("Содержание")
    order = models.PositiveIntegerField("Порядок", default=0)
    materials = models.FileField("Материалы", upload_to='lesson_materials/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} (Курс: {self.course.title})"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['order']

class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='homeworks', verbose_name="Урок")
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    due_date = models.DateTimeField("Срок сдачи", null=True, blank=True)

    def __str__(self):
        return f"{self.title} (Урок: {self.lesson.title})"

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"

class HomeworkSubmission(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='submissions', verbose_name="Студент")
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions', verbose_name="Домашнее задание")
    submission_date = models.DateTimeField("Дата сдачи", auto_now_add=True)
    grade = models.PositiveIntegerField("Оценка", null=True, blank=True)
    file = models.FileField("Файл с решением", upload_to='homework_submissions/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f"Задание {self.homework.title} от {self.student.user.first_name} {self.student.user.last_name} (ID: {self.id})"

    class Meta:
        verbose_name = "Сданное домашнее задание"
        verbose_name_plural = "Сданные домашние задания"

class HomeworkComment(models.Model):
    submission = models.ForeignKey(HomeworkSubmission, on_delete=models.CASCADE, related_name='comments', verbose_name="Сданное задание")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments', verbose_name="Автор")
    text = models.TextField("Текст комментария")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author.username if self.author else 'удаленный пользователь'} к заданию {self.submission.homework.title} (ID: {self.id})"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"