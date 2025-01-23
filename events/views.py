from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm
from events.models import Event, Category
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



# Dashboard Category
def deshboard_category(request):
    category = Category.objects.all()
    context = {"categories" : category}
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


def  delete_category(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, 'Category Deleted Successfully')
        return  redirect('dahsboard-category',)
    else:
        messages.error(request, 'Some thing went wrong')
        return  redirect('dahsboard-category')