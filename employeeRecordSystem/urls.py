from django.contrib import admin
from django.urls import path
from base import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('index',views.index,name='index'),
    path('addnewemp',views.signup, name='addnewemp'),
    path('signin',views.signin,name='signin'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('myprofile',views.myprofile,name='myprofile'),
    path('myattendance',views.myattendance,name='myattendance'),
    path('timein/',views.timein,name="timein"),
    path('timeout',views.timeout,name="timeout"),
    path('logout',views.logout,name='logout'),
    path('admin',views.adminlogin,name='admin'),
    path('sendemail',views.sendemail,name='sendemail'),
    path('sendemailatt',views.sendemailatt,name='sendemailatt'),
    path('sendemailpro',views.sendemailpro,name='sendemailpro'),
    path('adminMEdashboard',views.adminMEdashboard,name='adminMEdashboard'),
    path('edit/<slug:slug>',views.edit),
    path('update/<slug:slug>',views.update),
    path('delete/<slug:slug>',views.destroy),
    path('viewattendanceAdmin',views.viewattendanceAdmin,name='viewattendanceAdmin'),
    path('searchatt',views.searchatt,name='searchatt'),
    path('searchattStaff',views.searchattStaff,name='searchattStaff'),
    path('searchemp',views.searchemp,name='searchemp'),
    path('viewall',views.viewall,name='viewall'),
    path('sendemailadmin',views.sendemail2,name='sendemailadmin'),
    path('sendemailadmin2',views.sendemail22,name='sendemailadmin2'),


    
    
    # path('show',views.show,name='show')
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  