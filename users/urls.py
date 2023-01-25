from django.urls import path
from users import views


urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('', views.UsersListView.as_view(), name='users_list'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/change_pwd/', views.UserPassChangeView.as_view(), name='pass_change'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete')
]