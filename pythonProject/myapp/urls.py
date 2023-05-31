from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('',views.scrape_prices, name="scrape_prices"),
    path('admin/', admin.site.urls),
    ]