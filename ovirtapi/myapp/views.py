from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .models import *
from .func import *
from .forms import *
from requests.structures import CaseInsensitiveDict
import paramiko
from django.contrib.auth.decorators import login_required


def index(request):
    listusers = User_list.objects.all()
    context = {'listusers': listusers}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # print(username, password)
        if user is not None:
            login(request, user)
            print("if ", user)
            userpk = User_list.objects.filter(name=user)
            # print()
            context2 = {'pk': userpk[0].id}
            # print(id, id)
            # return HttpResponseRedirect("/users" + str(userpk[0].id))
            return render(request, 'myapp/profile.html', context2)
        print("непопал")
    return render(request, 'myapp/index.html', context)


def index_get_users_all(request):
    listusers = User_list.objects.all()
    context = {'listusers': listusers}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            print("if user")
            return HttpResponseRedirect("/user_info")

    return render(request, 'myapp/index.html', context)


def get_userid(request, pk):
    userlist = User_list.objects.get(id=pk)
    listusers = {}
    if (request.POST):
        login_data = request.POST.dict()
        if 'up' in login_data:
            manage_vm(login_data['up'], 'start', userlist.name, userlist.password)
        elif "down" in login_data:
            manage_vm(login_data['down'], 'stop', userlist.name, userlist.password)
    elif (request.GET):
        print("GET")

    body = get_vms_login(userlist.name, userlist.password)
    context = {'userlist': userlist, 'body': body}
    return render(request, 'myapp/get_userid.html', context)


def get_createvm(request, pk):
    userlist = User_list.objects.get(id=pk)
    body = get_vms_login(userlist.name, userlist.password)
    form = CreatevmForm()
    context = {'userlist': userlist, 'body': body, 'form': form}

    if request.method == 'POST':
        form = CreatevmForm(request.POST)
        if form.is_valid():
            # prin/t(frm.cleaned_data)
            create_vm(userlist.name, userlist.password, form.cleaned_data['name'], form.cleaned_data['cpu'],
                      form.cleaned_data['mem'], form.cleaned_data['hdd'], form.cleaned_data['template'])
            return HttpResponseRedirect("/users%i" % (int(pk)))
        else:
            form = CreatevmForm()

    return render(request, 'myapp/get_createvm.html', context)


def get_console(request):
    if (request.GET.get('mybtn')):
        print(request.GET)
        return render(request, 'myapp/get_console.html')


def delete_vm(request, pk, vm):
    userlist = User_list.objects.get(id=pk)
    listusers = {}
    pk = pk
    vm = vm
    if (request.POST):
        data = request.POST.dict()
        # print(data)
        if 'vm' in data:
            deletevm(data['vm'], pk, userlist.name, userlist.password)
            return HttpResponseRedirect("/users%i" % (int(pk)))

    # body = get_vms_login(userlist.name, userlist.password)
    context = {'userlist': userlist, 'vm': vm, 'pk': pk, }

    return render(request, 'myapp/delete.html', context)


def see_request(request):
    text = f"""
        Some attributes of the HttpRequest object:
        scheme: {request.scheme}
        path:   {request.path}
        method: {request.method}
        GET:    {request.GET}
        user:   {request.user}
    """
    return HttpResponse(text, content_type="text/plain")


# @login_required
def user_info(request):
    text = f"""
        Selected HttpRequest.user attributes:

        username:     {request.user.username}
        is_anonymous: {request.user.is_anonymous}
        is_staff:     {request.user.is_staff}
        is_superuser: {request.user.is_superuser}
        is_active:    {request.user.is_active}
    """

    return HttpResponse(text, content_type="text/plain")


# @allowed_users(allowed_roles=['contractor'])
# def userPage(request):
#     all_item = request.user.contractor.itemproject_set.all()
#
#     context = {'all_item': all_item}

@login_required(login_url='login')
def profile(request):
    text = f"""
        Selected HttpRequest.user attributes:
        scheme: {request.scheme}
        path:   {request.path}
        method: {request.method}
        GET:    {request.GET}
        user:   {request.user}
        username:     {request.user.username}
        is_anonymous: {request.user.is_anonymous}
        is_staff:     {request.user.is_staff}
        is_superuser: {request.user.is_superuser}
        is_active:    {request.user.is_active}
    """
    all_item = User_list.objects.get()
    print(all_item)
    context = {'all_item': all_item, 'text': text, }
    return render(request, 'myapp/profile.html', context)
