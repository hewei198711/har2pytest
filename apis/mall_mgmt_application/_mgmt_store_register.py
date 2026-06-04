import os

from util.client import client

data = {
    "customerType": 0,  # 客户类型，1/服务中心，2/服务公司
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_register(data=data, headers=headers):
    """
    服务中心在法大大注册
    /mgmt/store/register

    参数说明:
    - customerType: 客户类型，1/服务中心，2/服务公司
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/store/register"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
