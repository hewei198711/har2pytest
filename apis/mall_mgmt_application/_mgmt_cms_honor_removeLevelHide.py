import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_removeLevelHide(data=data, headers=headers):
    """
    移除用户荣誉(会员等级隐藏)名单
    /mgmt/cms/honor/removeLevelHide

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/honor/removeLevelHide"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
