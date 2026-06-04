import os

from util.client import client

data = {
    "productDtoList": [{"productCode": "", "productNum": 0, "productSecCode": ""}],  # 需要修改的商品
    "storeCode": "",  # 店铺中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_returnOrder_checkProductInventory(data=data, headers=headers):
    """
    店铺库存校验接口
    /mgmt/inventory/dis/mortgage/returnOrder/checkProductInventory

    参数说明:
    - productDtoList: 需要修改的商品
    - productDtoList.productCode: 商品一级编码
    - productDtoList.productNum: 商品数量(绝对值)
    - productDtoList.productSecCode: 商品二级编码(非定制品不要传此字段)
    - storeCode: 店铺中心编号
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/checkProductInventory"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
