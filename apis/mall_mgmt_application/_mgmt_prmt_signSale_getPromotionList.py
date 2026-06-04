import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_getPromotionList(params=params, headers=headers):
    """
    签约活动列表-签约购报表筛选条件使用
    /mgmt/prmt/signSale/getPromotionList

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/prmt/signSale/getPromotionList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
