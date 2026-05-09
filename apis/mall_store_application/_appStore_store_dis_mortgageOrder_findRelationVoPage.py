import os

from util.client import client

params = {
    "mortgageOrderId": 0,  # 押货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_findRelationVoPage(params=params, headers=headers):
    """
    查询商城-店铺、签约4.0押货单关联订单信息与出库状态
    /appStore/store/dis/mortgageOrder/findRelationVoPage

    参数说明:
    - mortgageOrderId: 押货单id
    """

    url = "/appStore/store/dis/mortgageOrder/findRelationVoPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
