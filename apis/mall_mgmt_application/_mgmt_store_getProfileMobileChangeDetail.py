import os

from util.client import client

params = {
    "id": 0,  # 资料变更ID
    "storeCode": "",  # 服务中心编码
    "type": 0,  # 电话变更类型：1/变更负责人手机号, 2/变更配偶手机号, 3/变更服务中心电话
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getProfileMobileChangeDetail(params=params, headers=headers):
    """
    获取服务中心手机号变更详情
    /mgmt/store/getProfileMobileChangeDetail

    参数说明:
    - id: 资料变更ID
    - storeCode: 服务中心编码
    - type: 电话变更类型：1/变更负责人手机号, 2/变更配偶手机号, 3/变更服务中心电话
    """

    url = "/mgmt/store/getProfileMobileChangeDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
