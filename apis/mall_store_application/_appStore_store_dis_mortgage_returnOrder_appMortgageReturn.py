import os

from util.client import client

data = {
    "productList": [{"mortgagePrice": 0.0, "productCode": "", "remark": "", "returnNum": 0}],  # 押货单商品列表信息
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemark": "",  # 一级原因备注
    "reasonSecond": "",  # 二级原因
    "reasonSecondId": 0,  # 二级原因id
    "reasonSecondRemark": "",  # 二级原因备注
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_returnOrder_appMortgageReturn(data=data, headers=headers):
    """
    APP押货退货下单
    /appStore/store/dis/mortgage/returnOrder/appMortgageReturn

    参数说明:
    - productList: 押货单商品列表信息
    - productList.mortgagePrice: 押货价
    - productList.productCode: 商品编码
    - productList.remark: 商品备注
    - productList.returnNum: 商品退货数量
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemark: 一级原因备注
    - reasonSecond: 二级原因
    - reasonSecondId: 二级原因id
    - reasonSecondRemark: 二级原因备注
    - storeCode: 服务中心编码
    """

    url = "/appStore/store/dis/mortgage/returnOrder/appMortgageReturn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
