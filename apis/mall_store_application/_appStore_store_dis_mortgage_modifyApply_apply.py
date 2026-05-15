import os

from util.client import client

data = {
    "orderSn": "",  # 押货单编号
    "products": [{"mortgageNum": 0, "productCode": ""}],  # 修改明细
    "reason": "",  # 申请原因
    "remarks": "",  # 修改说明
    "storeCode": "",  # 服务中心编号(无需填写)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_modifyApply_apply(data=data, headers=headers):
    """
    提交修改申请
    /appStore/store/dis/mortgage/modifyApply/apply

    参数说明:
    - orderSn: 押货单编号
    - products: 修改明细
    - products.mortgageNum: 商品数量
    - products.productCode: 商品编号
    - reason: 申请原因
    - remarks: 修改说明
    - storeCode: 服务中心编号(无需填写)
    """

    url = "/appStore/store/dis/mortgage/modifyApply/apply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
