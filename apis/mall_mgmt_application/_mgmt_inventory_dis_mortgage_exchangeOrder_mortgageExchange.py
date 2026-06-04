import os

from util.client import client

data = {
    "exchangeType": 0,  # 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    "files": [{"fileName": "", "fileUrl": ""}],  # 换货单附件，支持3个
    "productList": [
        {
            "dailyUseType": 0,
            "disposalType": 0,
            "exchangeNum": 0,
            "firstUseTime": "",
            "happenType": 0,
            "problemDesc": "",
            "productBatch": "",
            "productCode": "",
            "productProvenance": "",
            "productSn": "",
            "productionDate": "",
            "restrictedDate": "",
        }
    ],  # TODO: 添加参数说明
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemark": "",  # 一级原因备注
    "reasonSecond": "",  # 二级原因
    "reasonSecondId": 0,  # 二级原因id
    "reasonSecondRemark": "",  # 二级原因备注
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_exchangeOrder_mortgageExchange(data=data, headers=headers):
    """
    押货换货下单
    /mgmt/inventory/dis/mortgage/exchangeOrder/mortgageExchange

    参数说明:
    - exchangeType: 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    - files: 换货单附件，支持3个
    - files.fileName: 换货单附件url
    - files.fileUrl: 换货单附件url
    - productList.dailyUseType: 日常使用时间 1早上 2中午 3晚上
    - productList.disposalType: 旧品处理方式 1服务中心报废 2分公司报废 3退货中转仓 4分公司自行处理
    - productList.exchangeNum: 物品换货数
    - productList.firstUseTime: 第一次使用的时间
    - productList.happenType: 物品问题发生状态 1初次开封使用发现 2使用过程中发现
    - productList.problemDesc: 问题描述
    - productList.productBatch: 批次号
    - productList.productCode: 商品编号
    - productList.productProvenance: 商品产地
    - productList.productSn: 物品序列号/二维码
    - productList.productionDate: 物品生产日期
    - productList.restrictedDate: 物品限用日期
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemark: 一级原因备注
    - reasonSecond: 二级原因
    - reasonSecondId: 二级原因id
    - reasonSecondRemark: 二级原因备注
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/dis/mortgage/exchangeOrder/mortgageExchange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
