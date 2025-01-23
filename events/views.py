from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from events.forms import EventModelForm
from events.models import Event
# Create your views here.

def home_page(request):
    return  render(request, 'Home/home.html',)

def  dashboard_page(request):
    events = Event.objects.all()
    context = {"events" : events}
    return  render(request, 'dashboard/dashboard-event.html', context)

# Create Event
def create_event(request):
    event_form = EventModelForm()
    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request,"Event Created Successfully")
            return redirect('create-event')
    context = {"form" : event_form}
    return render(request, 'create-event.html', context)

#Update Event
def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('update-event', id)
    context = {"form" : event_form, "id": id}
    return render(request, 'create-event.html', context)

# Delete Event

def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return  redirect('dahsboard')
    else:
        messages.error(request, 'Some thing went wrong')
        return  redirect('dahsboard')
