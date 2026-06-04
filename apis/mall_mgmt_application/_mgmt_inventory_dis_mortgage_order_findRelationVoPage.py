import os

from util.client import client

params = {
    "mortgageOrderId": 0,  # 押货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_findRelationVoPage(params=params, headers=headers):
    """
    查询商城-店铺、签约4.0押货单关联订单信息与出库状态
    /mgmt/inventory/dis/mortgage/order/findRelationVoPage

    参数说明:
    - mortgageOrderId: 押货单id
    """

    url = "/mgmt/inventory/dis/mortgage/order/findRelationVoPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
