import os

from util.client import client

data = {
    "adjustBatchNo": "",  # 调整批次号
    "cardNo": "",  # 会员卡号
    "effectiveEndTime": "",  # 生效结束时间
    "effectiveStartTime": "",  # 生效开始时间
    "from": 0,  # TODO: 添加参数说明
    "increaseEndTime": "",  # 增加结束时间
    "increaseStartTime": "",  # 增加开始时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "reduceEndTime": "",  # 扣减结束时间
    "reduceStartTime": "",  # 扣减开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_getAdjustedList(data=data, headers=headers):
    """
    信用额调整记录表-列表
    /mgmt/fin/wallet/credit/getAdjustedList

    参数说明:
    - adjustBatchNo: 调整批次号
    - cardNo: 会员卡号
    - effectiveEndTime: 生效结束时间
    - effectiveStartTime: 生效开始时间
    - increaseEndTime: 增加结束时间
    - increaseStartTime: 增加开始时间
    - pageNum: 页数
    - pageSize: 每页显示数
    - reduceEndTime: 扣减结束时间
    - reduceStartTime: 扣减开始时间
    """

    url = "/mgmt/fin/wallet/credit/getAdjustedList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
