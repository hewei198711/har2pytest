import os

from util.client import client

data = {
    "auditRemark": "",  # 备注
    "auditStatus": 0,  # 审核结果：1：提交审核；2：已通过；3：不通过；7：待提交
    "creditAdjustBatchId": 0,  # 调整批次id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_submitAdjustBatch(data=data, headers=headers):
    """
    信用额调整批次-提交审核
    /mgmt/fin/wallet/credit/submitAdjustBatch

    参数说明:
    - auditRemark: 备注
    - auditStatus: 审核结果：1：提交审核；2：已通过；3：不通过；7：待提交
    - creditAdjustBatchId: 调整批次id
    """

    url = "/mgmt/fin/wallet/credit/submitAdjustBatch"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
