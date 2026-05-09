import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_checkMallSignOrderStatus(params=params, headers=headers):
    """
    查询(包括2.0/3.0/4.0)签约单状态 1->待签约 2->已签约 3->已履约 4->已解约 5->已取消
    /appStore/store/dis/mortgageOrder/checkMallSignOrderStatus

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/store/dis/mortgageOrder/checkMallSignOrderStatus"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
