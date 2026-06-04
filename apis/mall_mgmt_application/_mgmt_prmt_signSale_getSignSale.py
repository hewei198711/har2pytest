import os

from util.client import client

params = {
    "promotionId": 0,  # promotionId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_getSignSale(params=params, headers=headers):
    """
    内容中心获取已关联的签约购活动信息
    /mgmt/prmt/signSale/getSignSale

    参数说明:
    - promotionId: promotionId
    """

    url = "/mgmt/prmt/signSale/getSignSale"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
