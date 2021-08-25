from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<str:product_title>/detail",views.detail, name='detail'),
    path("watch_list",views.watch_list,name='watch_list'),
    path("update_watch_list",views.update_watch_list,name='update_watch_list'),
    path("bid", views.bid,name='bid'),
    path("close_auction", views.close_auction, name='close_auction'),
    path("categories", views.categories,name='categories'),
    path("comment", views.comment,name='comment'),
]
