from django.urls import path
from . import views

urlpatterns = [

    # MVC urls
    path('', views.index, name='index'),
    path('register', views.register, name="register"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('dataentry', views.data_entry, name="dataentry"),
    path('orders', views.show_orders, name="orders"),
    path('operator', views.show_all_orders, name="operator"),
    path('deliveryman', views.show_delivery_orders, name="deliveryman"),
    path('assign_deliveryman', views.assign_deliveryman, name="assign_deliveryman"),
    path('finish_order', views.finish_order, name="finish_order"),
    path('editprofile', views.edit_profile, name="editprofile"),
    path('resetpwd', views.reset_pwd, name="resetpwd"),

    # API urls
    path('itemedit', views.edit_item, name="itemedit"),
    path('mkorder', views.make_order, name="mkorder")
]