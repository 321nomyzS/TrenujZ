from django.urls import path
import dashboard.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercise/add', views.add_exercise, name='add_exercise'),
    path('exercise', views.show_exercises, name='show_exercises'),
    path('exercise/<id>', views.show_exercise, name='show_exercise'),
    path('exercise/delete/<id>/', views.delete_exercise, name='delete_exercise'),
    path('edit_exercise/<id>/', views.edit_exercise, name='edit_exercise'),
    path('training/add', views.add_training, name='add_training'),
    path('training', views.show_trainings, name='show_trainings'),
    path('training/duplicate/<id>', views.duplicate_training, name='duplicate_training'),
    path('training/<id>', views.show_training, name='show_training'),
    path('training/edit/<id>', views.edit_training, name='edit_training'),
    path('training/delete/<id>', views.delete_training, name='delete_training'),
    path('user/add', views.add_user, name='add_user'),
    path('user', views.show_users, name='show_users'),
    path('user/<id>', views.show_user, name='show_user'),
    path('client/edit/<id>', views.edit_user, name='edit_user'),
    path('user/delete/<id>', views.delete_user, name='delete_user'),
    path('tag', views.show_tags, name='show_tags'),
    path('tag/add', views.add_tag, name='add_tag'),
    path('tag/<id>', views.show_tag, name='show_tag'),
    path('tag/edit/<id>', views.edit_tag, name='edit_tag'),
    path('tag/delete/<id>', views.delete_tag, name='delete_tag'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_tunnel, name='logout_tunnel')
]