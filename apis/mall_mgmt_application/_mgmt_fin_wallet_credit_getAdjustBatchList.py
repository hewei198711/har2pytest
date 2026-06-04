import os

from util.client import client

data = {
    "adjustBatchNo": "",  # 调整批次号
    "auditStatus": 0,  # 审核状态：1：待审核；2：已通过；3：已驳回；7：待提交
    "batchStatus": 0,  # 批次状态：1：未生效；2：已扣减；3：已增加
    "entryEndTime": "",  # 录入结束时间
    "entryStartTime": "",  # 录入开始时间
    "from": 0,  # TODO: 添加参数说明
    "increaseEndTime": "",  # 增加结束时间
    "increaseStartTime": "",  # 增加开始时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_getAdjustBatchList(data=data, headers=headers):
    """
    信用额调整批次-列表
    /mgmt/fin/wallet/credit/getAdjustBatchList

    参数说明:
    - adjustBatchNo: 调整批次号
    - auditStatus: 审核状态：1：待审核；2：已通过；3：已驳回；7：待提交
    - batchStatus: 批次状态：1：未生效；2：已扣减；3：已增加
    - entryEndTime: 录入结束时间
    - entryStartTime: 录入开始时间
    - increaseEndTime: 增加结束时间
    - increaseStartTime: 增加开始时间
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/fin/wallet/credit/getAdjustBatchList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
