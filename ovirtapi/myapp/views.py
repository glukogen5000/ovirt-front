from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .models import *
from .func import *
from .forms import *
from requests.structures import CaseInsensitiveDict
import paramiko
from django.contrib.auth.decorators import login_required


def index(request):  # отрисовка главной страницы

    context = {}

    if request.method == 'POST':  # аутентификация
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # print(username, password)
        if user is not None:
            login(request, user)
            context2 = {'username': user.id}
            return render(request, 'myapp/index.html', context2)
        else:
            pass
    return render(request, 'myapp/index.html', context)



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
    if (request.POST):
        login_data = request.POST.dict()
        if 'up' in login_data:
            manage_vm(login_data['up'], 'start', all_item.name, all_item.password)
        elif "down" in login_data:
            manage_vm(login_data['down'], 'stop', all_item.name, all_item.password)
        elif "delete" in login_data:
            deletevm(login_data['delete'], all_item.name, all_item.password)


    elif (request.GET):
        print("GET")
    #
    body = get_vms_login(all_item.name, all_item.password)

    context = {'all_item': all_item, 'text': text, 'body': body, }
    return render(request, 'myapp/profile.html', context)



def get_createvm(request):
    all_item = User_list.objects.get()
    body = get_vms_login(all_item.name, all_item.password)
    form = CreatevmForm()
    context = {'all_item': all_item, 'body': body, 'form': form}

    if request.method == 'POST':
        form = CreatevmForm(request.POST)
        if form.is_valid():
            # prin/t(frm.cleaned_data)
            create_vm(all_item.name, all_item.password, form.cleaned_data['name'], form.cleaned_data['cpu'],
                      form.cleaned_data['mem'], form.cleaned_data['hdd'], form.cleaned_data['template'],
                      form.cleaned_data['vm_hostname'], form.cleaned_data['vm_username'], form.cleaned_data['vm_password'])
            return HttpResponseRedirect('/profile')
        else:
            form = CreatevmForm()

    return render(request, 'myapp/get_createvm.html', context)