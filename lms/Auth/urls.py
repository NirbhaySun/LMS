from django.urls import path
from .views import login, register, logout

urlpatterns =[
    path('login/',login,name='login'),
    path('register/',register,name ='register'),
    path('logout/', logout, name='logout'),
    # path('delete-all-users/', delete_all_users, name='delete_all_users'),
]