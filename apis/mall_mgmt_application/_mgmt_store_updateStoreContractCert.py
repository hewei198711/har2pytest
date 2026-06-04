import os

from util.client import client

data = {
    "adminIdCard": "",  # 法大大管理员身份证
    "adminMobile": "",  # 企业管理员手机号
    "adminName": "",  # 企业管理员名称
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_updateStoreContractCert(data=data, headers=headers):
    """
    修改电子印章认证信息
    /mgmt/store/updateStoreContractCert

    参数说明:
    - adminIdCard: 法大大管理员身份证
    - adminMobile: 企业管理员手机号
    - adminName: 企业管理员名称
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/updateStoreContractCert"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
