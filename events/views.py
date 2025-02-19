from django.shortcuts import render, redirect
from django.contrib import messages
from events.forms import EventModelForm, CategoryModelForm
from events.models import Event, Category 
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from  users.views import is_admin, is_organizer, is_participant
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

User = get_user_model()
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

# Create Event Class Based View
class CreateEventView(ContextMixin,LoginRequiredMixin,View):
    login_url = 'sign-in'
    template_name = 'create-event.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', EventModelForm())
        return context
    
    # GET  
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    # POST
    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request,"Event Created Successfully")
            return redirect('create-event')
        
    

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

#Update Event Class Based View
class UpdateEventView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'create-event.html'
    pk_url_kwarg = 'id'
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event_form = EventModelForm(request.POST,request.FILES, instance=self.object)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('update-event', self.object.id)
        
    


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
    
# Delete Event Class Based View
class DeleteEventView(LoginRequiredMixin, DeleteView):
    model = Event
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('dashboard') 
    
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(request, "Event Deleted Successfully")
            
        except Exception as e:
            messages.error(request, f"An Error occurred: {e}")
        
        return HttpResponseRedirect(self.success_url)
            


# Event Details 
def event_details(request, event_id):
    event = Event.objects.get(id= event_id)
    
    return render(request, 'event_details.html', {'event': event})

# Event Details Class Based View
class EventDetailsView(DetailView):
    model = Event
    template_name = 'event_details.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'
    

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


# Create Category Class Based View
class CreateCategoryView(ContextMixin,LoginRequiredMixin,View):
    login_url = 'sign-in'
    template_name = 'create-category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', CategoryModelForm())
        return context
    
    # GET  
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    # POST
    def post(self, request, *args, **kwargs):
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,"Category Created Successfully")
            return redirect('create-category')
    

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

# Update Category Class Based View

class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'create-category.html'
    pk_url_kwarg = 'id'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        category_form = CategoryModelForm(request.POST, instance=self.object)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,"Category update Successfully")
            return redirect('update-category', self.object.id)
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


# Delete Category  Class Based View
class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('categories-list') 
    
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(request, "Category Deleted Successfully ✅✅✅")
            
        except Exception as e:
            messages.error(request, f"An Error occurred: {e}")
        
        return HttpResponseRedirect(self.success_url)


  




    
    
  