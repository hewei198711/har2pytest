import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "queryParam": "",  # queryParam
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_getPromotion(params=params, headers=headers):
    """
    根据活动编码或活动名称查询签约购活动,用于关联登陆提醒与内容中心
    /mgmt/prmt/signSale/getPromotion

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - queryParam: queryParam
    """

    url = "/mgmt/prmt/signSale/getPromotion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
