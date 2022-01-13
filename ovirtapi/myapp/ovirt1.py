import requests
import json
import bs4


#
#
# def get_key(username, passwd):
#     response = requests.get(
#         'https://ovirt2-engine.test.local/ovirt-engine/sso/oauth/token', verify=False,
#         params={'grant_type': 'password',
#                 'scope': 'ovirt-app-api',
#                 'username': username,
#                 'password': passwd},
#         headers={'Accept': 'application/json',
#                  'Content-Type': 'application/x-www-form-urlencoded'})
#     todos = json.loads(response.text)
#     return (todos['access_token'])
#
#
# def get_datacenter():
#     response = requests.get(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/datacenters', verify=False,
#
#         headers={'Accept': 'application/xml',
#
#                  'Authorization': 'Bearer ' + get_key('admin@internal', '1412Flvby')},
#     )
#     if response.status_code == 200:
#         soup = bs4.BeautifulSoup(response.text, 'lxml')
#         dc_list = [x.get_text(strip=True) for x in soup.select('name')]
#         return dc_list
#
#
# def get_vms():
#     response = requests.get(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms', verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Authorization': 'Bearer ' + get_key('admin@internal', '1412Flvby')},
#     )
#     if response.status_code == 200:
#         soup = bs4.BeautifulSoup(response.text, 'lxml')
#         x = soup.findAll("vm")
#         vm_name = {}
#         for item in x:
#             z = item.find('name').text
#             r = item.get('id')
#             zx = item.find('status').text
#             ip = item.find('address')
#             if ip:
#                 ip = ip.text
#             vm_name[z] = r, zx, ip
#         return vm_name
#
#
# # x=get_vms()
# # print(type(x))
# # for item
#
# # import requests
# # from requests.structures import CaseInsensitiveDict
# #
# # url = "https://ovirt2-engine.test.local/ovirt-engine/api/vms"
# #
# # headers = CaseInsensitiveDict()
# # headers["Version"] = "4"
# # headers["Content-Type"] = "application/xml"
# # headers["Accept"] = "application/xml"
# # headers["Authorization"] = "Bearer "+ get_key('admin@internal', '1412Flvby')
# #
# # data = """
# #
# # <action>
# #   <vm>
# #     <os>
# #
# #     </os>
# #   </vm>
# # </action>
# #
# #
# # """
# #
# #
# #     resp = requests.post(url, headers=headers, data=data, verify=False,)
#
# # print(get_key('admin@internal', '1412Flvby'))
#
# import paramiko
#
#
# def create_user_ovirt(key1, key2):
#     host = 'ovirt2-engine.test.local'
#     user = 'root'
#     secret = '1412Flvby'
#     port = 22
#
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(hostname=host, username=user, password=secret, port=port)
#     rum_command = 'ovirt-aaa-jdbc-tool user add ' + key1 + ' --attribute=firstName=John --attribute=lastName=Doe && ' \
#                                                            'ovirt-aaa-jdbc-tool user password-reset ' + key1 + ' --password=pass:' + key2 + ' --password-valid-to="2025-08-01 12:00:00-0800"'
#     stdin, stdout, stderr = client.exec_command(rum_command)
#
#     data = stdout.read() + stderr.read()
#     client.close()
#     return print(data)
#
#
# create_user_ovirt('test2', 'ES935dpi')
from requests.auth import HTTPBasicAuth


def get_token(username, passwd):
    response = requests.get(
        'https://ovirt2-engine.test.local/ovirt-engine/api', verify=False, auth=HTTPBasicAuth(username,passwd),
        params={},
        headers={'Accept': 'application/json',
                 'prefer': 'persistent-auth',
                 'Content-Type': 'application/xml',
                  })

    # key = json.loads(response.text)
    return print(response.text)



get_token('user3@internal', 'ES935dpi')
