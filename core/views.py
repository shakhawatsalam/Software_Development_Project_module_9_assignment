from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event
from django.db.models import Q
# Create your views here.
def home(request):
    search_value= request.GET.get('search')
    if search_value:
        events = Event.objects.filter(Q(name__icontains=search_value) | Q(location__icontains=search_value))
    else:
        events = Event.objects.all()
    context ={"events" : events}
    return render(request, 'home.html',context)


def no_permission(request):
    return render(request, 'no_permission.html')