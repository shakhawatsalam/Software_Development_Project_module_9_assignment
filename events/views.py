from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from events.models import Event, Category , Participant
from datetime import date, timedelta
from django.db.models import Q, Count, Max, Min, Avg
# Create your views here.

def home_page(request):
    search_value= request.GET.get('search')
    if search_value:
        events = Event.objects.filter(Q(name__icontains=search_value) | Q(location__icontains=search_value))
    else:
        events = Event.objects.all()
    context ={"events" : events}
    return  render(request, 'Home/home.html' ,context)

# 
def dashboard_grid(request) :
    
    return  render(request, 'dashboard/dashboard.html',)
# All Event
def  dashboard_page(request):
    
    counts =  Event.objects.aggregate(
        total_participant = Count('events',distinct=True),
        total_events = Count('id',distinct=True),
        upcoming_events =Count('id', filter=Q(date__gt= date.today())),
        past_events =Count('id', filter=Q(date__lt=date.today()))  
    )
    type = request.GET.get('type', 'all')

    if type == 'total_events':
        events = Event.objects.all().annotate(
            total_participant=Count('events', distinct=True)
        ) 
    if type == 'upcoming_events':
        events = Event.objects.filter(date__gt= date.today()).annotate(
            total_participant=Count('events', distinct=True)
        ) 
    if type == 'past_events':
        events = Event.objects.filter(date__lt= date.today()).annotate(
            total_participant=Count('events', distinct=True)
        ) 
    if type == 'all':
        events = Event.objects.filter(date=date.today()).annotate(
            total_participant=Count('events', distinct=True)
        ) 
        
    context = {"events" : events, "counts": counts}
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



# Dashboard Category
def deshboard_category(request):
    category = Category.objects.all()
    context = {"categories" : category, }
    return  render(request, 'dashboard/dashboard-category.html', context)
# Create Category
def create_category(request):
    category_form = CategoryModelForm()
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,"Category Created Successfully")
            return redirect('create-category')
    context = {"form" : category_form}
    return render(request, 'create-category.html', context)

# Update Category
def update_category(request,  id):
    category = Category.objects.get(id=id)
    category_form = CategoryModelForm(instance=category)
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,"Category update Successfully")
            return redirect('update-category', id)
    context = {"form" : category_form, "id" :  id}
    return render(request, 'create-category.html', context)

# Delete Category
def  delete_category(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, 'Category Deleted Successfully')
        return  redirect('dahsboard-category',)
    else:
        messages.error(request, 'Some thing went wrong')
        return  redirect('dahsboard-category')



# Dashboard Category
def deshboard_participant(request):
    participant = Participant.objects.all()
    context = {"participants" : participant}
    return  render(request, 'dashboard/dashboard-participant.html', context)
  
# Create participant
def create_participant(request):
    participant_form = ParticipantModelForm()
    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request,"Participant Created Successfully")
            return redirect('create-participant')
    context = {"form" : participant_form}
    return render(request, 'create-participant.html', context)


# Update participant
def update_participant(request,id):
    participant = Participant.objects.get(id=id)
    participant_form = ParticipantModelForm(instance=participant)
    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST, instance=participant)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request,"Participant Updated Successfully")
            return redirect('update-participant', id)
    context = {"form" : participant_form, "id" :  id}
    return render(request, 'create-participant.html', context)
    
    
# Delete Category
def  delete_participant(request,id):
    if request.method == 'POST':
        participant = Participant.objects.get(id=id)
        participant.delete()
        messages.success(request, 'Participant Deleted Successfully')
        return  redirect('dahsboard-participant',)
    else:
        messages.error(request, 'Some thing went wrong')
        return  redirect('dahsboard-participant')    