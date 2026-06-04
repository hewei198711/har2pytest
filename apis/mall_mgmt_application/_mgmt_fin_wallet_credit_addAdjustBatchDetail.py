import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "creditAdjustBatchNo": "",  # 调整批次号
    "creditAdjustBatchdetailId": 0,  # 调整批次详情id，新增不传，修改必传
    "increaseAmount": 0.0,  # 本次增加信用额
    "increaseEndTime": "",  # 增加结束时间
    "increaseStartTime": "",  # 增加开始时间
    "reduceAmount": 0.0,  # 本次扣减信用额
    "reduceTime": "",  # 扣减时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_addAdjustBatchDetail(data=data, headers=headers):
    """
    信用额调整批次详情-新增
    /mgmt/fin/wallet/credit/addAdjustBatchDetail

    参数说明:
    - cardNo: 会员卡号
    - creditAdjustBatchNo: 调整批次号
    - creditAdjustBatchdetailId: 调整批次详情id，新增不传，修改必传
    - increaseAmount: 本次增加信用额
    - increaseEndTime: 增加结束时间
    - increaseStartTime: 增加开始时间
    - reduceAmount: 本次扣减信用额
    - reduceTime: 扣减时间
    """

    url = "/mgmt/fin/wallet/credit/addAdjustBatchDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
