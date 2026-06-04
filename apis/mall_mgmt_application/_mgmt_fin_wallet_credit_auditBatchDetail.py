import os

from util.client import client

data = {
    "auditRemark": "",  # 审核备注
    "auditStatus": 0,  # 审批状态：7，待提交，1，待审核，2，审核通过，9，审核不通过。不传查全部
    "batchId": 0,  # 批次ID
    "idList": [],  # 批次详情ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_auditBatchDetail(data=data, headers=headers):
    """
    云商信用额录入批次详情列表提交审核
    /mgmt/fin/wallet/credit/auditBatchDetail

    参数说明:
    - auditRemark: 审核备注
    - auditStatus: 审批状态：7，待提交，1，待审核，2，审核通过，9，审核不通过。不传查全部
    - batchId: 批次ID
    - idList: 批次详情ID
    """

    url = "/mgmt/fin/wallet/credit/auditBatchDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
