import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_checkSignOrderV3Status(params=params, headers=headers):
    """
    查询签约3.0状态 1->待签约 2->已签约 3->已履约 4->已解约 5->已取消
    /appStore/store/dis/mortgageOrder/checkSignOrderV3Status

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/store/dis/mortgageOrder/checkSignOrderV3Status"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
