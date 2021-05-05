from django.urls import path
from . import views

urlpatterns = [

    # MVC urls
    path('', views.index, name='index'),
    path('register', views.register, name="register"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('dataentry', views.data_entry, name="dataentry"),

    # API urls
    path('itemedit', views.edit_item, name="itemedit")
]