from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:pk>/", views.listings, name="listings"),
    path("listings/<int:pk>/bid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listings/<int:pk>/comment", views.comment, name="comment"),
    path("listings/<int:pk>/close", views.close, name="close"),
    path("remove/<int:pk>/", views.remove, name="remove"),
    path("add/<int:pk>/", views.add, name="add")
]
