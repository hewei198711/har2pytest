import os

from util.client import client

data = {
    "cancelTime": "",  # 取消时间
    "discountPermission": "",  # 85%权限
    "frozenReason": "",  # 冻结原因
    "frozenTime": "",  # 冻结时间
    "permission": "",  # 1:3权限
    "shopType": 0,  # 权限
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_updatePermission(data=data, headers=headers):
    """
    服务中心权限编辑修改
    /mgmt/store/updatePermission

    参数说明:
    - cancelTime: 取消时间
    - discountPermission: 85%权限
    - frozenReason: 冻结原因
    - frozenTime: 冻结时间
    - permission: 1:3权限
    - shopType: 权限
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/updatePermission"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
