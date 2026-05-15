import os

from util.client import client

params = {
    "id": 0,  # 资料变更ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_profileCredentialChangeDetail_id(params=params, headers=headers):
    """
    获取服务中心证件信息变更详情
    /appStore/store/profile/profileCredentialChangeDetail/{id}

    参数说明:
    - id: 资料变更ID
    """

    url = f"/appStore/store/profile/profileCredentialChangeDetail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
