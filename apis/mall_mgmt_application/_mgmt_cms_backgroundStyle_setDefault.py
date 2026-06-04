import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_backgroundStyle_setDefault(data=data, headers=headers):
    """
    设置默认背景样式
    /mgmt/cms/backgroundStyle/setDefault

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/backgroundStyle/setDefault"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
