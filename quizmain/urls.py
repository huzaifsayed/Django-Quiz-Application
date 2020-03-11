"""quizmain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from apps.frontend.views import HomeView, QuizMaker, QuizDelete, QuizTakerView, QuizTakerHomeView
from apps.backend.views import Dashboard, QuestionsDisplay, QuestionsCreate, QuestionsDelete
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #Front END
    path('', HomeView.as_view(), name='homepage'),

    path('about-us/', TemplateView.as_view(template_name="frontend/aboutus.html"), name='aboutus'),
    path('contact-us/', TemplateView.as_view(template_name="frontend/contactus.html"), name='contactus'),
    path('privacy-policy/', TemplateView.as_view(template_name="frontend/privacypolicy.html"), name='privacypolicy'),


    path('quiz/', QuizMaker.as_view(), name='quizmaking'),
    #Back ENd
    path('quizlogin/', auth_views.LoginView.as_view(
        template_name='common/login.html'
        ), 
        name='login'
    ),
    path('quizlogout/', auth_views.LogoutView.as_view(
        next_page='login'
        ), 
        name='logout'
    ),
    path('quizdashboard/', Dashboard.as_view(), name='dashboard'),
    path('questions/', QuestionsDisplay.as_view(), name='questions'),
    path('questions/create', QuestionsCreate.as_view(), name='questionscreate'),
    path('questions/delete/<int:pk>', QuestionsDelete.as_view(), name='questionsdelete'),
    path('quiz/delete/<int:pk>', QuizDelete.as_view(), name='quizdelete'),
    path('quiz/<slug>/<name>', QuizTakerView.as_view(), name='quiztakerhome'),
    path('quiz/<slug>', QuizTakerHomeView.as_view(), name='quiztaker'),

    
    
]
