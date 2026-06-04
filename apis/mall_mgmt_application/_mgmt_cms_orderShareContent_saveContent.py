import os

from util.client import client

data = {
    "content": "",  # 内容文案
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_orderShareContent_saveContent(data=data, headers=headers):
    """
    新增订单分享文案
    /mgmt/cms/orderShareContent/saveContent

    参数说明:
    - content: 内容文案
    """

    url = "/mgmt/cms/orderShareContent/saveContent"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
