import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_orderShareContent_getList(headers=headers):
    """
    获取订单分享内容配置列表
    /mgmt/cms/orderShareContent/getList
    """

    url = "/mgmt/cms/orderShareContent/getList"
    with client.get(url=url, headers=headers) as r:
        return r
