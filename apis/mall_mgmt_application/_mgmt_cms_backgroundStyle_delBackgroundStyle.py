import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_backgroundStyle_delBackgroundStyle(data=data, headers=headers):
    """
    删除背景样式
    /mgmt/cms/backgroundStyle/delBackgroundStyle

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/backgroundStyle/delBackgroundStyle"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
