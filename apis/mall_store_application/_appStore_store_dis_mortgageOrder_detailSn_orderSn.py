import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_detailSn_orderSn(params=params, headers=headers):
    """
    押货单详情(编号查询)
    /appStore/store/dis/mortgageOrder/detailSn/{orderSn}

    参数说明:
    - orderSn: orderSn
    """

    url = f"/appStore/store/dis/mortgageOrder/detailSn/{params['orderSn']}"
    with client.get(url=url, headers=headers) as r:
        return r
