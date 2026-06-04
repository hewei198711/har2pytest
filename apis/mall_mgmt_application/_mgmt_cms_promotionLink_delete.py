import os

from util.client import client

data = {
    "id": 0,  # 第三方软件推广链接id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promotionLink_delete(data=data, headers=headers):
    """
    删除指定id的第三方软件推广链接
    /mgmt/cms/promotionLink/delete

    参数说明:
    - id: 第三方软件推广链接id
    """

    url = "/mgmt/cms/promotionLink/delete"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
