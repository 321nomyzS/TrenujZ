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
    path('training', views.show_training, name='show_training'),
    path('training/duplicate/<id>', views.duplicate_training, name='duplicate_training'),
    path('training/general/<id>', views.show_general_training, name='show_general_training'),
    path('training/personal/<id>', views.show_personal_training, name='show_personal_training'),
    path('training/general/edit/<id>', views.edit_general_training, name='edit_general_training'),
    path('training/personal/edit/<id>', views.edit_personal_training, name='edit_personal_training'),
    path('training/general/delete/<id>', views.delete_general_training, name='delete_general_training'),
    path('training/personal/delete/<id>', views.delete_personal_training, name='delete_personal_training'),
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