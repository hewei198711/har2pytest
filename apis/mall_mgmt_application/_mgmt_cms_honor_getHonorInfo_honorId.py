import os

from util.client import client

params = {
    "honorId": 0,  # honorId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_getHonorInfo_honorId(params=params, headers=headers):
    """
    获取用户荣誉称号信息
    /mgmt/cms/honor/getHonorInfo/{honorId}

    参数说明:
    - honorId: honorId
    """

    url = f"/mgmt/cms/honor/getHonorInfo/{params['honorId']}"
    with client.get(url=url, headers=headers) as r:
        return r
