
from django.urls import path
from .views import CourseListView, CourseDetailView, LessonDetail


app_name = "courses"

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('<slug>', CourseDetailView.as_view(), name='detail'),
    #url(r'(P<slug>[\w-]+') same thing as up
    path("<course_slug>/<lesson_slug>", LessonDetail.as_view(), name="lesson_detail")
    ]
