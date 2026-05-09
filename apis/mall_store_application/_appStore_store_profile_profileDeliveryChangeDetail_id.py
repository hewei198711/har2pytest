import os

from util.client import client

params = {
    "id": "",  # 资料变更ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_profileDeliveryChangeDetail_id(params=params, headers=headers):
    """
    获取服务中心收货信息变更详情
    /appStore/store/profile/profileDeliveryChangeDetail/{id}

    参数说明:
    - id: 资料变更ID
    """

    url = f"/appStore/store/profile/profileDeliveryChangeDetail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
