from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from datetime import datetime
from . import forms, views


urlpatterns = [

    path('', views.start, name='home'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('login/',
         LoginView.as_view
             (
             template_name='main/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('regist/', views.regist, name='regist'),
    path('begin/', views.begin, name='begin'),
    path('begin2/', views.begin2, name='begin2'),
    path('begin3/', views.begin3, name='begin3'),
    path('begin4/', views.begin4, name='begin4'),
    path('zada4i_tems/', views.zada4i_tems, name='zada4i_tems'),
    path('zada4i/', views.zada4i, name='zada4i'),
    path('table/', views.table, name='table'),
    path('developers/', views.developers, name='developers'),
    path('instruction/', views.instruction, name='instruction'),
    # path('teacherStart/', views.teacherStart, name='teacherStart'),
    path('studentStart/', views.studentStart, name='studentStart'),
    path('teacherTask/', views.teacherTask, name='teacherTask'),
    path('teacherReg/', views.teacherReg, name='teacherReg'),
    path('teacherRegist/', views.teacherRegist, name='teacherRegist'),
    path('change_password/', views.change_password, name='change_password'),
    path('createWork/', views.createWork, name='createWork'),
    path('Zada4iStud/', views.Zada4iStud, name='Zada4iStud'),
    path('studentStat/', views.studentStat, name='studentStat'),
    path('StartToCheck/', views.StartToCheck, name='StartToCheck'),
    path('TeacherCheckStat/', views.TeacherCheckStat, name='TeacherCheckStat'),
    path('studentItogStat/', views.studentItogStat, name='studentItogStat'),
    path('error/', views.error, name='error'),
    path('workStatus/', views.workStatus, name='workStatus'),
    path('error2/', views.error2, name='error2'),
    path('error3/', views.error3, name='error3'),
    path('startToCheck2/', views.startToCheck2, name='startToCheck2'),
    path('summary_of_work/', views.summary_of_work, name='summary_of_work'),
    path('CheckStartWork/', views.CheckStartWork, name='CheckStartWork'),
    path('predCheckStartWork/', views.predCheckStartWork, name='predCheckStartWork'),
    path('kubok/', views.kubok, name='kubok'),
    path('workCreated/', views.workCreated, name='workCreated'),
]

### urls идут по последовательности их создания