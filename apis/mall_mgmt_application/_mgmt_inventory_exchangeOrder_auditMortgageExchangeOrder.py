import os

from util.client import client

data = {
    "auditFileName": "",  # 审批附件名称
    "auditFileUrl": "",  # 审批附件
    "auditRemarks": "",  # 审批备注
    "auditStatus": 0,  # 审批意见 0不通过 1通过
    "exchangeType": 0,  # 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    "id": 0,  # TODO: 添加参数说明
    "productDisposalType": 0,  # 旧品处理方式 1服务中心报废 2分公司报废 3退货中转仓 4分公司自行处理
    "productVoList": [
        {
            "dailyUseType": 0,
            "firstUseTime": "",
            "happenType": 0,
            "id": 0,
            "productBatch": 0,
            "productDisposalType": 0,
            "productNum": 0,
            "productProblemDesc": "",
            "productProductionDate": "",
            "productProvenance": "",
            "productSn": "",
        }
    ],  # TODO: 添加参数说明
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemarks": "",  # 一级原因备注
    "reasonSecond": "",  # 二级原因
    "reasonSecondId": 0,  # 二级原因id
    "reasonSecondRemarks": "",  # 二级原因备注
    "returnInfo": "",  # 退回信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_exchangeOrder_auditMortgageExchangeOrder(data=data, headers=headers):
    """
    后台审批押货换货单
    /mgmt/inventory/exchangeOrder/auditMortgageExchangeOrder

    参数说明:
    - auditFileName: 审批附件名称
    - auditFileUrl: 审批附件
    - auditRemarks: 审批备注
    - auditStatus: 审批意见 0不通过 1通过
    - exchangeType: 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    - productDisposalType: 旧品处理方式 1服务中心报废 2分公司报废 3退货中转仓 4分公司自行处理
    - productVoList.dailyUseType: 日常使用时间 1早上 2中午 3晚上
    - productVoList.firstUseTime: 第一次使用的时间
    - productVoList.happenType: 物品问题发生状态 1初次开封使用发现 2使用过程中发现
    - productVoList.id: 物品记录id
    - productVoList.productBatch: 批次号
    - productVoList.productDisposalType: 旧品处理方式 1服务中心报废 2分公司报废 3退货中转仓 4分公司自行处理
    - productVoList.productNum: 物品换货数
    - productVoList.productProblemDesc: 问题描述
    - productVoList.productProductionDate: 物品生产日期
    - productVoList.productProvenance: 商品产地
    - productVoList.productSn: 物品序列号/二维码
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemarks: 一级原因备注
    - reasonSecond: 二级原因
    - reasonSecondId: 二级原因id
    - reasonSecondRemarks: 二级原因备注
    - returnInfo: 退回信息
    """

    url = "/mgmt/inventory/exchangeOrder/auditMortgageExchangeOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
