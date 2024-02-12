from calendar import HTMLCalendar, day_abbr
from django.urls import reverse
from events.models import Event
from calendar import monthrange

class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(day__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            events_html += f'<li>{event.title}</li>'
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return f'<td class="{self.cssclasses[weekday]}">{day}{events_html}</td>'

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        events = Event.objects.filter(day__year=theyear, day__month=themonth)

        v = []
        a = v.append
        a('<table border="1" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')

        last_day = monthrange(theyear, themonth)[1]
        days_in_month = range(1, last_day + 1)
        for week in self.monthdays2calendar(theyear, themonth):
            week = [(day, wd) if day in days_in_month else (0, wd) for day, wd in week]
            a(self.formatweek(week, events))
            a('\n')

        a('</table>')
        a('\n')

        

        return ''.join(v)

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name.
        """
        # 한글로 월 표시
        s = '%s년 %s월' % (theyear, themonth)
        if withyear:
            return '<tr><th colspan="7" class="month">%s</th></tr>' % s
        return '<tr><th colspan="7" class="month">%s</th></tr>' % s

    def formatweekheader(self):
        """
        Return a header for a week.
        """
        # 한글로 요일 표시
        header = ['월', '화', '수', '목', '금', '토', '일']
        return '<tr>%s</tr>' % ''.join('<th class="%s">%s</th>' % (self.cssclasses[weekday], day) for (weekday, day) in enumerate(header))

    def get_previous_month(self, theyear, themonth):
        if themonth == 1:
            return theyear - 1, 12
        else:
            return theyear, themonth - 1

    def get_next_month(self, theyear, themonth):
        if themonth == 12:
            return theyear + 1, 1
        else:
            return theyear, themonth + 1
