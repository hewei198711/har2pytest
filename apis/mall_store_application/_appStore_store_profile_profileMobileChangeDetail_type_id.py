import os

from util.client import client

params = {
    "type": "",  # 变更类型，1/变更负责人手机号, 2/变更配偶手机号, 3/变更服务中心电话
    "id": "",  # 资料变更ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_profileMobileChangeDetail_type_id(params=params, headers=headers):
    """
    获取服务中心手机号变更详情
    /appStore/store/profile/profileMobileChangeDetail/{type}/{id}

    参数说明:
    - id: 资料变更ID
    - type: 变更类型，1/变更负责人手机号, 2/变更配偶手机号, 3/变更服务中心电话
    """

    url = f"/appStore/store/profile/profileMobileChangeDetail/{params['type']}/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
