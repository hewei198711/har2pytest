import os
from urllib.parse import urlencode

from util.client import client

data = {
    "companyName": "",  # companyName
    "isImport": False,  # isImport
    "operationName": "",  # operationName
    "operationStaff": "",  # operationStaff
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_dataAdmin_warningWhiteList_import(data=data, headers=headers):
    """
    导入文件-导入预警白名单
    /mgmt/dataAdmin/warningWhiteList/import

    参数说明:
    - companyName: companyName
    - isImport: isImport
    - operationName: operationName
    - operationStaff: operationStaff
    """

    url = "/mgmt/dataAdmin/warningWhiteList/import"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
