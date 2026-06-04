import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getLinkProductInfo(params=params, headers=headers):
    """
    根据关联商品编码获取商品信息
    /mgmt/cms/getLinkProductInfo

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/cms/getLinkProductInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
