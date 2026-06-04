import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "diffWay": 0,  # 处理方案，1：扣减相应金额；2：补回相应金额
    "from": 0,  # TODO: 添加参数说明
    "handleBatch": "",  # 处理批次号
    "handleStatus": 0,  # 处理状态，1：待处理；2：已处理
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "sourceOrderNo": "",  # 来源订单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_exportDiffList(data=data, headers=headers):
    """
    导出秒返券调差列表
    /mgmt/fin/voucher/second/coupon/exportDiffList

    参数说明:
    - cardNo: 会员卡号
    - diffWay: 处理方案，1：扣减相应金额；2：补回相应金额
    - handleBatch: 处理批次号
    - handleStatus: 处理状态，1：待处理；2：已处理
    - pageNum: 页数
    - pageSize: 每页显示数
    - sourceOrderNo: 来源订单号
    """

    url = "/mgmt/fin/voucher/second/coupon/exportDiffList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
