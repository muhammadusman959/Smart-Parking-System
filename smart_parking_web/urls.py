from django.contrib import admin
from django.urls import path
from parking_gui import views  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Homepage -> Show Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Buttons -> Trigger Logic
    path('allocate/', views.process_allocation, name='process_allocation'),
    path('undo/', views.process_undo, name='process_undo'),
    path('release/', views.process_release, name='process_release'),
]