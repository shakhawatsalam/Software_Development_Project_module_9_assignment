from django.shortcuts import render, redirect
from users.forms import RegistrationForm, LoginForm, AssignedRoleForm, CreateGroupForm, UpdateUserForm
from django.contrib.auth  import login, logout
from django.contrib import  messages
from django.contrib.auth.models import User, Group
from events.models import Event, Category
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.db.models import Prefetch



# CHECKING USER'S ROLE
# Test for users
def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_organizer(user):
    return user.groups.filter(name='organizer').exists()
def is_participant(user):
    return user.groups.filter(name='participants').exists()

def is_organizer_or_admin(user):
    return is_organizer(user) or is_admin(user)


# SIGN-UP / REGISTER
def sign_up(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request, 'A Confirmation mail sent. Please Check your Email')
            return redirect('sign-in')
    return render(request, 'registration/register.html', {"form" :  form})
# ACTIVATE USER
def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if  default_token_generator.check_token(user,  token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        
        else:
            return HttpResponse('Invalid Id or Token')
    except User.DoesNotExist:
        return HttpResponse('User not found')
# SIGN-IN / LOG IN
def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {"form" :  form})

# SIGN-OUT / LOG OUT
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    
# ADMIN DASHBOARD ----> VIEW'S
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    events = Event.objects.all()
    context = {
        "events": events
    }
    return render(request, 'admin/dashboard.html', context)

# ALL USER LIST
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def admin_view_userlist(request):
    users= User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')                               
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/user_list.html', {"users": users})
    
# ASSIGN ROLE 
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignedRoleForm()
    if request.method == 'POST':
        form = AssignedRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin-view-userlist')
    return render(request, 'admin/assign_role.html', {"form" : form})



# CREATE GROUP
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group {group.name} has been created successfully')
            return redirect('group-list')
    return render(request, 'admin/create_group.html', {'form': form})


# VIEW ALL GROUP
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {"groups": groups})


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, group_id):
    if request.method == 'POST':
        group = Group.objects.get(id = group_id)
        group.delete()
        messages.success(request, f' Group Name: {group.name} Deleted Successfully')
        return  redirect('group-list')
    else:
        messages.error(request, 'Some thing went wrong')
        return  redirect('group-list')

# VIEW ALL PARTICIPANTS
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def admin_view_participantlist(request):
    try:
        participant_group = Group.objects.get(name="participants")
        
        users = participant_group.user_set.all()
    except Group.DoesNotExist:
        users = User.objects.none()
    
    return render(request, 'admin/participant_list.html', {"users": users})

# UPDATE PARTICIPANT
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def update_participants(request, user_id):
    user = User.objects.get(id = user_id)
    form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant Updated Successfully")
            return redirect('participant-list')
    return render(request,'admin/update_user.html', {"form": form})


# DELETE PARTICIPANT
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_participants(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, 'User Deleted Successfully')
        return  redirect('participant-list')
    else:
        messages.error(request, 'Some thing went wrong')
        return  redirect('participant-list')
    
 
# ORGANIZER DASHBOARD ----> VIEW'S
@login_required
@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    events = Event.objects.all()
    context = {
        "events": events
    }
    return render(request,'organizer/dashboard.html', context)
 
# VIEW ALL CATEGORIES
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')     
def categories_list(request):
    categories = Category.objects.all()
    context={"categories" : categories}
    
    return render(request, 'organizer/categories_list.html', context)


# PARTICIPANTS DASHBOARD ----> VIEW'S
# EVENT'S THAT ARE LOGIN USER PARTICIPATE
@login_required
@user_passes_test(is_participant, login_url='no-permission')   
def participants_dashboard(request):
    print(request.user)
    events = Event.objects.filter(participants=request.user)
    context = {
        "events": events
    }
    return render(request,'participants/dashboard.html', context)



# REDIRECTING USER ACCORDING  TO ROLE 
def dashboard(request):
    if is_participant(request.user):
        return redirect('participants-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    return redirect('no-permission')