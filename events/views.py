from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from .utils import EventCalendar
from .models import Event

def event_list(request):
    events = Event.objects.all()
    today = timezone.now()
    cal = EventCalendar(events).formatmonth(today.year, today.month)
    return render(request, 'events/event_list.html', {'calendar': cal, 'events': events})

def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def calendar_view(request, year=None, month=None):
    today = timezone.now()
    if year and month:
        today = today.replace(year=int(year), month=int(month))
    events = Event.objects.all()
    cal = EventCalendar(events).formatmonth(today.year, today.month)
    
    prev_month = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
    next_month = (today.year, today.month + 1) if today.month < 12 else (today.year + 1, 1)
    prev_url = reverse('events:calendar_view_with_month', kwargs={'year': prev_month[0], 'month': prev_month[1]})
    next_url = reverse('events:calendar_view_with_month', kwargs={'year': next_month[0], 'month': next_month[1]})
    
    return render(request, 'events/calendar_view.html', {'calendar': cal, 'events': events, 'prev_url': prev_url, 'next_url': next_url})


def get_previous_month_calendar(request):
    today = timezone.now()
    prev_month = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
    events = Event.objects.filter(day__year=prev_month[0], day__month=prev_month[1])
    cal = EventCalendar(events).formatmonth(prev_month[0], prev_month[1])  
    return JsonResponse({'calendar_html': cal})

def get_next_month_calendar(request):
    today = timezone.now()
    next_month = (today.year, today.month + 1) if today.month < 12 else (today.year + 1, 1)
    events = Event.objects.filter(day__year=next_month[0], day__month=next_month[1])
    cal = EventCalendar(events).formatmonth(next_month[0], next_month[1]) 
    return JsonResponse({'calendar_html': cal})