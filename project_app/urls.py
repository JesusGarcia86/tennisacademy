from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logreg', views.logreg),
    path('create_user', views.register),
    path('log_in', views.log_in),
    path('member', views.success),
    path('about', views.about),
    path('coach', views.coach),
    path('tutorials', views.tutorials),
    path('virtual', views.virtual),
    path('forum', views.forum),
    path('logout', views.logout),
    path('contact', views.contactView),
    path('success/', views.successView),
    path('purchase', views.purchase),
    path('charge', views.charge),
    path('like/<int:user_id>', views.add_like),
    path('create_message', views.create_mess),
    path('delete/<int:mess_id>', views.delete_mess),
    path('no_access', views.no_access),
    path('newlog', views.newlog),
    path('sign_up', views.sign_up),
    path('sign_in', views.sign_in),
    path('create_comment', views.create_comm),
    path('comm_delete/<int:comm_id>', views.delete_comm),
]