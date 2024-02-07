from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('calendar/', views.calendar_view, name='calendar_view'),  
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_view_with_month'),
    path('get_previous_month_calendar/', views.get_previous_month_calendar, name='get_previous_month_calendar'),
    path('get_next_month_calendar/', views.get_next_month_calendar, name='get_next_month_calendar'),
]
