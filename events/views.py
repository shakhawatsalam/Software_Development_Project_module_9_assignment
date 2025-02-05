from django.shortcuts import render, redirect
from django.contrib import messages
from events.forms import EventModelForm, CategoryModelForm
from events.models import Event, Category 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from  users.views import is_admin, is_organizer, is_participant

def is_organizer_or_admin(user):
    return is_organizer(user) or is_admin(user)

# 
def dashboard_grid(request) :
    return  render(request, 'dashboard/dashboard.html',)
# All Event
def  dashboard_page(request):
    
    # counts =  Event.objects.aggregate(
    #     total_participant = Count('events',distinct=True),
    #     total_events = Count('id',distinct=True),
    #     upcoming_events =Count('id', filter=Q(date__gt= date.today())),
    #     past_events =Count('id', filter=Q(date__lt=date.today()))  
    # )
    # type = request.GET.get('type', 'all')

    # if type == 'total_events':
    #     events = Event.objects.all().annotate(
    #         total_participant=Count('events', distinct=True)
    #     ) 
    # if type == 'upcoming_events':
    #     events = Event.objects.filter(date__gt= date.today()).annotate(
    #         total_participant=Count('events', distinct=True)
    #     ) 
    # if type == 'past_events':
    #     events = Event.objects.filter(date__lt= date.today()).annotate(
    #         total_participant=Count('events', distinct=True)
    #     ) 
    # if type == 'all':
    #     events = Event.objects.filter(date=date.today()).annotate(
    #         total_participant=Count('events', distinct=True)
    #     ) 
        
    # context = {"events" : events, "counts": counts}
    return  render(request, 'dashboard/dashboard-event.html')

# Create Event
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def create_event(request):
    event_form = EventModelForm()
    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request,"Event Created Successfully")
            return redirect('create-event')
    context = {"form" : event_form}
    return render(request, 'create-event.html', context)

#Update Event
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
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
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return  redirect('dashboard')
    else:
        messages.error(request, 'Some thing went wrong')
        return  redirect('dashboard')


# Event Details 
def event_details(request, event_id):
    event = Event.objects.get(id= event_id)
    
    return render(request, 'event_details.html', {'event': event})

# RSVP EVENT
@login_required
def rsvp_event(request, event_id, user_id):
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=user_id)
    if event.participants.filter(pk=user.pk).exists():
        messages.error(request, "You have already registered for this event!")
    else:
        event.participants.add(user)
        messages.success(request, "You have successfully registered for the event!")
    return redirect('event-details', event_id=event_id)


# Dashboard Category
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def deshboard_category(request):
    category = Category.objects.all()
    context = {"categories" : category, }
    return  render(request, 'dashboard/dashboard-category.html', context)
# Create Category
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def create_category(request):
    category_form = CategoryModelForm()
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,"Category Created Successfully")
            return redirect('categories-list')
    context = {"form" : category_form}
    return render(request, 'create-category.html', context)

# Update Category
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
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
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def  delete_category(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, 'Category Deleted Successfully')
        return  redirect('categories-list',)
    else:
        messages.error(request, 'Some thing went wrong')
        return  redirect('categories-list')




  




    
    
  