from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


# app_name = "auctions"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("insert_listing",views.insert_listing,name="insert_listing"),
    path("create_listing",views.create_listing,name="create_listing"),
    path("listing/<int:id>/",views.listing,name="listing"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("watchlist/<int:pk>", views.watchlist, name="watchlist"),  
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 