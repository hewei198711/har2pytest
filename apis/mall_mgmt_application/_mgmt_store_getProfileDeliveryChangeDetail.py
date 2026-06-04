import os

from util.client import client

params = {
    "id": 0,  # 资料变更ID
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getProfileDeliveryChangeDetail(params=params, headers=headers):
    """
    获取服务中心收货信息变更详情
    /mgmt/store/getProfileDeliveryChangeDetail

    参数说明:
    - id: 资料变更ID
    - storeCode: 服务中心编码
    """

    url = "/mgmt/store/getProfileDeliveryChangeDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
