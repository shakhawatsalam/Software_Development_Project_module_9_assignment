from django.urls import path
from events.views import dashboard_page, home_page, create_event, update_event, delete_event

urlpatterns = [
    path('home/', home_page, name='home'),
    path('dashboard/', dashboard_page, name='dahsboard'),
    path('create-event/', create_event, name='create-event'),
    path('update-event/<int:id>', update_event, name='update-event'),
    path('delete-event/<int:id>', delete_event, name='delete-event'),
]