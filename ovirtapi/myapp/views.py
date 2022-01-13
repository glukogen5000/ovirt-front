from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .models import *
from .func import *
from .forms import *
from requests.structures import CaseInsensitiveDict
import paramiko
from django.contrib.auth.decorators import login_required

def get_bearer_key(username, password):
    response = requests.get(
        'https://ovirt2-engine.test.local/ovirt-engine/sso/oauth/token', verify=False,
        params={'grant_type': 'password',
                'scope': 'ovirt-app-api',
                'username': username,
                'password': password},
        headers={'Accept': 'application/json',
                 'Content-Type': 'application/x-www-form-urlencoded'})
    bearer_key = json.loads(response.text)
    return (bearer_key['access_token'])



def get_vms_login(username, password):
    response = requests.get(
            'https://ovirt2-engine.test.local/ovirt-engine/api/vms', verify=False,

            headers={'Accept': 'application/xml',
                     'Authorization': 'Bearer ' + get_bearer_key(username, password)})

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        all_virt_machine = soup.findAll("vm")
        vm_name = {}
        for item in all_virt_machine:
            comment = item.find('comment').text
            id = item.get('id')
            status = item.find('status').text
            ip = item.find('address')
            if ip:
                ip = ip.text
            vm_name[id] = comment, status, ip
        return (vm_name)

    else:
        print(response.status_code)



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

    # if (request.POST):
    #     login_data = request.POST.dict()
    #     if 'up' in login_data:
    #         manage_vm(login_data['up'], 'start', all_item.name, all_item.password)
    #     elif "down" in login_data:
    #         manage_vm(login_data['down'], 'stop', all_item.name, all_item.password)
    # elif (request.GET):
    #     print("GET")
    #
    body = get_vms_login(all_item.name, all_item.password)
    #body = {'1': 1, '2': 2, '21231232': 3, '123123123': 4}
    context = {'all_item': all_item, 'text': text, 'body': body, }
    return render(request, 'myapp/profile.html', context)

#
# def get_userid(request, pk):
#     userlist = User_list.objects.get(id=pk)
#     listusers = {}
#
#
#     body = get_vms_login(userlist.name, userlist.password)
#     context = {'userlist': userlist, 'body': body}
#     return render(request, 'myapp/profile.html', context)
#
#
# def get_createvm(request, pk):
#     userlist = User_list.objects.get(id=pk)
#     body = get_vms_login(userlist.name, userlist.password)
#     form = CreatevmForm()
#     context = {'userlist': userlist, 'body': body, 'form': form}
#
#     if request.method == 'POST':
#         form = CreatevmForm(request.POST)
#         if form.is_valid():
#             # prin/t(frm.cleaned_data)
#             create_vm(userlist.name, userlist.password, form.cleaned_data['name'], form.cleaned_data['cpu'],
#                       form.cleaned_data['mem'], form.cleaned_data['hdd'], form.cleaned_data['template'])
#             return HttpResponseRedirect("/users%i" % (int(pk)))
#         else:
#             form = CreatevmForm()
#
#     return render(request, 'myapp/get_createvm.html', context)
#
#
# def get_console(request):
#     if (request.GET.get('mybtn')):
#         print(request.GET)
#         return render(request, 'myapp/get_console.html')
#
#
# def delete_vm(request, pk, vm):
#     userlist = User_list.objects.get(id=pk)
#     listusers = {}
#     pk = pk
#     vm = vm
#     if (request.POST):
#         data = request.POST.dict()
#         # print(data)
#         if 'vm' in data:
#             deletevm(data['vm'], pk, userlist.name, userlist.password)
#             return HttpResponseRedirect("/users%i" % (int(pk)))
#
#     # body = get_vms_login(userlist.name, userlist.password)
#     context = {'userlist': userlist, 'vm': vm, 'pk': pk, }
#
#     return render(request, 'myapp/delete.html', context)
