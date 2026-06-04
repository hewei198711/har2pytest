import os

from util.client import client

data = {
    "expireDate": "",  # 结束有效期
    "id": 0,  # id
    "maxDownloadTimes": 0,  # 可下载次数
    "startDate": "",  # 起始有效期
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "templateNo": "",  # 授权书模板编号
    "year": "",  # 授权书年份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_editAuthorizationLetter(data=data, headers=headers):
    """
    修改授权书
    /mgmt/store/authorization/editAuthorizationLetter

    参数说明:
    - expireDate: 结束有效期
    - id: id
    - maxDownloadTimes: 可下载次数
    - startDate: 起始有效期
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - templateNo: 授权书模板编号
    - year: 授权书年份
    """

    url = "/mgmt/store/authorization/editAuthorizationLetter"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
