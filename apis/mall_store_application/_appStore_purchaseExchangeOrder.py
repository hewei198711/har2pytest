import os

from util.client import client

data = {
    "orderFileName": "",  # 换货单附件名称，支持3个，用逗号隔开
    "orderFileUrl": "",  # 换货单附件，支持3个，用逗号隔开
    "productVoList": [
        {
            "dailyUseType": 0,
            "firstUseTime": "",
            "happenType": 0,
            "productBatch": "",
            "productCode": "",
            "productNum": 0,
            "productProblemDesc": "",
            "productProductionDate": "",
            "productProvenance": "",
            "productRestrictedDate": "",
            "productSn": "",
        }
    ],  # 商品列表
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemarks": "",  # 一级原因备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseExchangeOrder(data=data, headers=headers):
    """
    添加换货单
    /appStore/purchaseExchangeOrder

    参数说明:
    - orderFileName: 换货单附件名称，支持3个，用逗号隔开
    - orderFileUrl: 换货单附件，支持3个，用逗号隔开
    - productVoList: 商品列表
    - productVoList.dailyUseType: 日常使用时间只能为 1早上 2中午 3晚上
    - productVoList.firstUseTime: 第一次使用的时间
    - productVoList.happenType: 物品问题发生状态只能是 1初次开封使用发现 2使用过程中发现
    - productVoList.productBatch: 批次号
    - productVoList.productCode: 商品编号
    - productVoList.productNum: 商品换货数
    - productVoList.productProblemDesc: 问题描述
    - productVoList.productProductionDate: 生产日期/有效期
    - productVoList.productProvenance: 商品产地
    - productVoList.productRestrictedDate: 限用日期
    - productVoList.productSn: 物品序列号/二维码
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemarks: 一级原因备注
    """

    url = "/appStore/purchaseExchangeOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
