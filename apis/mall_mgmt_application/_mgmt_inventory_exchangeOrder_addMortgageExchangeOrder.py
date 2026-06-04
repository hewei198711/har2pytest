import os

from util.client import client

data = {
    "exchangeType": 0,  # 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    "orderFileName": "",  # 换货单附件名，支持3个，用逗号隔开
    "orderFileUrl": "",  # 换货单附件，支持3个，用逗号隔开
    "productVoList": [
        {
            "dailyUseType": 0,
            "firstUseTime": "",
            "happenType": 0,
            "productBatch": "",
            "productCode": "",
            "productDisposalType": 0,
            "productMortgagePrice": 0.0,
            "productNum": 0,
            "productProblemDesc": "",
            "productProductionDate": "",
            "productProvenance": "",
            "productRestrictedDate": "",
            "productRetailPrice": 0.0,
            "productSn": "",
        }
    ],  # TODO: 添加参数说明
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemarks": "",  # 一级原因备注
    "reasonSecond": "",  # 二级原因
    "reasonSecondId": 0,  # 二级原因id
    "reasonSecondRemarks": "",  # 二级原因备注
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_exchangeOrder_addMortgageExchangeOrder(data=data, headers=headers):
    """
    后台申请添加押货换货单
    /mgmt/inventory/exchangeOrder/addMortgageExchangeOrder

    参数说明:
    - exchangeType: 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    - orderFileName: 换货单附件名，支持3个，用逗号隔开
    - orderFileUrl: 换货单附件，支持3个，用逗号隔开
    - productVoList.dailyUseType: 日常使用时间 1早上 2中午 3晚上
    - productVoList.firstUseTime: 第一次使用的时间
    - productVoList.happenType: 物品问题发生状态 1初次开封使用发现 2使用过程中发现
    - productVoList.productBatch: 批次号
    - productVoList.productCode: 物品编号
    - productVoList.productDisposalType: 旧品处理方式 1服务中心报废 2分公司报废 3退货中转仓 4分公司自行处理
    - productVoList.productMortgagePrice: 物品押货价
    - productVoList.productNum: 物品换货数
    - productVoList.productProblemDesc: 问题描述
    - productVoList.productProductionDate: 物品生产日期
    - productVoList.productProvenance: 商品产地
    - productVoList.productRestrictedDate: 物品限用日期
    - productVoList.productRetailPrice: 物品零售价
    - productVoList.productSn: 物品序列号/二维码
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemarks: 一级原因备注
    - reasonSecond: 二级原因
    - reasonSecondId: 二级原因id
    - reasonSecondRemarks: 二级原因备注
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/exchangeOrder/addMortgageExchangeOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
