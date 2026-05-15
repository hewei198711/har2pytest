import os

from util.client import client

data = {
    "applyType": 0,  # 提交途径 1门店提交 2后台提交
    "productList": [{"eightFivePrice": 0.0, "oneThreePrice": 0.0, "productCode": "", "transferNum": 0}],  # 商品明细
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disInventoryTransfer_addTransfer(data=data, headers=headers):
    """
    新建库存转移记录
    /appStore/store/disInventoryTransfer/addTransfer

    参数说明:
    - applyType: 提交途径 1门店提交 2后台提交
    - productList: 商品明细
    - productList.eightFivePrice: 85折押货价
    - productList.oneThreePrice: 1:3押货价
    - productList.productCode: 产品编号
    - productList.transferNum: 转移数量
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/disInventoryTransfer/addTransfer"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
