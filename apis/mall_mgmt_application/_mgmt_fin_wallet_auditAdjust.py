import os

from util.client import client

data = {
    "auditRemark": "",  # 审批意见
    "status": 0,  # 审批结果:2：已通过；3：已驳回；6：已撤回；
    "walletAdjustId": 0,  # 钱包调整id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_auditAdjust(data=data, headers=headers):
    """
    手工录入款项审核-审核
    /mgmt/fin/wallet/auditAdjust

    参数说明:
    - auditRemark: 审批意见
    - status: 审批结果:2：已通过；3：已驳回；6：已撤回；
    - walletAdjustId: 钱包调整id
    """

    url = "/mgmt/fin/wallet/auditAdjust"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
