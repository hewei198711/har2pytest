import os

from util.client import client

data = {
    "creditStagesCode": "",  # 信用额分期编码
    "eachReduceAmt": 0.0,  # 每期扣减金额
    "remark": "",  # 调整备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_editCreditStagesData(data=data, headers=headers):
    """
    信用分期管理编辑
    /mgmt/fin/wallet/credit/stages/editCreditStagesData

    参数说明:
    - creditStagesCode: 信用额分期编码
    - eachReduceAmt: 每期扣减金额
    - remark: 调整备注
    """

    url = "/mgmt/fin/wallet/credit/stages/editCreditStagesData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
