import requests
import json
import bs4
import uuid

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render


def disk_create(vm_name, hdd_size, namedisk):
    text = f"""
        <disk_attachment>
            <bootable>true</bootable>
            <interface>virtio</interface>
            <active>true</active>
            <disk>        
                <description>disk{vm_name}</description>
                <format>cow</format>
                <name>{namedisk}</name>
                <provisioned_size>{hdd_size}</provisioned_size>
                <storage_domains>
                    <storage_domain id="0b27fe8c-cbe3-4657-bfe9-4083ab6aab3b"/>
                </storage_domains>
            </disk>
        </disk_attachment>"""
    return text


def lan_create():
    text = f"""
        <nic>
            <name>lan</name>
            <interface>virtio</interface>
            <vnic_profile href="/ovirt-engine/api/vnicprofiles/2ecfee9d-632c-433f-8de3-c848bb64b4bf" id="2ecfee9d-632c-433f-8de3-c848bb64b4bf" />
        </nic>"""
    return text










def get_key(username, password):
    response = requests.get(
        'https://ovirt2-engine.test.local/ovirt-engine/sso/oauth/token', verify=False,
        params={'grant_type': 'password',
                'scope': 'ovirt-app-api',
                'username': username,
                'password': password},
        headers={'Accept': 'application/json',
                 'Content-Type': 'application/x-www-form-urlencoded'})
    key = json.loads(response.text)
    return (key['access_token'])


def get_datacenter():
    response = requests.get(
        'https://ovirt2-engine.test.local/ovirt-engine/api/datacenters', verify=False,

        headers={'Accept': 'application/xml',

                 'Authorization': 'Bearer ' + get_key('', '')},
    )
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        dc_list = [x.get_text(strip=True) for x in soup.select('name')]
        return dc_list


# def get_vms():
#     response = requests.get(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms', verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Authorization': 'Bearer ' + get_key('admin@internal', '')},
#     )
#     if response.status_code == 200:
#         soup = bs4.BeautifulSoup(response.text, 'lxml')
#         x = soup.findAll("vm")
#         vm_name = {}
#         for item in x:
#             z = item.find('name').text
#             r = item.get('id')
#             status = item.find('status').text
#             url_stop = item.find("link", {"rel": "stop"})['href']
#             # print(the_url)
#             vm_name[z] = r, status, url_stop
#
#         return vm_name


def manage_vm(vmid, run, username, password):
    data = """<action/>"""
    response = requests.post(
        'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vmid + '/' + run, data=data, verify=False,

        headers={'Accept': 'application/xml',
                 'Content-Type': 'application/xml',
                 'Authorization': 'Bearer ' + get_key(username, password)},
    )
    if response.status_code == 200:
        return


def get_vms_login(username, password):
    response = requests.get(
        'https://ovirt2-engine.test.local/ovirt-engine/api/vms', verify=False,

        headers={'Accept': 'application/xml',
                 'Authorization': 'Bearer ' + get_key(username, password)},
    )
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        all_vms_user = soup.findAll("vm")
        vm_info = {}
        for vm in all_vms_user:
            vm_comment = vm.find('comment').text
            vm_id = vm.get('id')
            vm_status = vm.find('status').text
            vm_url_stop = vm.find("link", {"rel": "stop"})['href']
            # print(url_stop)
            vm_info[vm_id] = vm_comment, vm_status, vm_url_stop

        # print(vm_info)
        return vm_info


# def create_user_ovirt(username,password):
#     host = 'ovirt2-engine.test.local '
#     user = username
#     secret = password
#     port = 22
#
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(hostname=host, username=user, password=secret, port=port)
#     stdin, stdout, stderr = client.exec_command('ls -l')
#     data = stdout.read() + stderr.read()
#     client.close()
#     return print(data)


# def index(request):
#     if (request.POST):
#         login_data = request.POST.dict()
#         if 'up' in login_data:
#             manage_vm(login_data['up'], 'start')
#         elif "down" in login_data:
#             manage_vm(login_data['down'], 'stop')
#
#     return render(request, 'myapp/index.html', {'body': get_vms})
def deletevm(vm_name, username, passwd):
    response = requests.delete(
        'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vm_name, verify=False,

        headers={'Accept': 'application/xml',
                 'Content-Type': 'application/xml',
                 'Authorization': 'Bearer ' + get_key(username, passwd)},
    )


def create_vm(username, passwd, vm_name, cpu, mem, hdd, template):
    data = f"""
            <vm>
            <name>{uuid.uuid4()}</name>
            <comment>{vm_name}</comment>
            <cluster>
                <name>cl1</name>
            </cluster>
            <template>
                <name>{template}</name>
            </template>
            <memory>{mem}</memory>
    		<memory_policy>
    		    <ballooning>true</ballooning>
    		    <guaranteed>536870912</guaranteed>
    		    <max>{mem}</max>
    		</memory_policy>
            <os>
                <boot dev="hd"/>
            </os>
            <cpu_profile id="02eb3942-9669-440c-a282-72fee895776d"/>
            	<initialization>
                     <cloud_init>
                  <host>
                     <address>myhost.mydomain.com</address>
                  </host>
                     <users>
                        <user>
                        <user_name>root</user_name>
                      <password>root</password>
                         </user>
                        </users>
	         </cloud_init>
        </initialization>
    	</vm>
        """
    # print(data)
    # print(data2)

    response = requests.post(
        'https://ovirt2-engine.test.local/ovirt-engine/api/vms', verify=False,

        headers={'Accept': 'application/xml',
                 'Content-Type': 'application/xml',
                 'Authorization': 'Bearer ' + get_key(username, passwd)},
        data=data,

    )
    if response.status_code == 201 or response.status_code == 202:
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        all_vms_user = soup.findAll("vm")
        vm_info = {}
        for vm in all_vms_user:
            vm_comment = vm.find('comment').text
            vm_id = vm.get('id')
            vm_status = vm.find('status').text
            vm_url_stop = vm.find("link", {"rel": "stop"})['href']
            # print(url_stop)
            vm_info[vm_id] = vm_comment, vm_status, vm_url_stop
            data2 =disk_create(vm_id, hdd, vm_comment)
            responsehdd = requests.post(
                'https://ovirt2-engine.test.local/ovirt-engine/api/vms/'+ vm_id+'/diskattachments', verify=False,

                headers={'Accept': 'application/xml',
                         'Content-Type': 'application/xml',
                         'Authorization': 'Bearer ' + get_key(username, passwd)},
                data=data2,
            )
            datalan = lan_create()
            responselan = requests.post(
                'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vm_id + '/nics', verify=False,

                headers={'Accept': 'application/xml',
                         'Content-Type': 'application/xml',
                         'Authorization': 'Bearer ' + get_key(username, passwd)},
                data=datalan,
            )


        return


def get_console_vnc(vm_id, username, passwd):
    responsevnc = requests.post(
        'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vm_id + '/graphicsconsoles', verify=False,

        headers={'Accept': 'application/xml',
                 'Content-Type': 'application/xml',
                 'Authorization': 'Bearer ' + get_key(username, passwd)},

    )
    # print(responsevnc.text)




def create_disk(*args):
    return print(*args)


def connect_lan(*args):
    return
