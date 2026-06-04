import os

from util.client import client

data = {
    "auditRemark": "",  # 审批备注
    "remittanceRemark": "",  # 汇款备注
    "status": 0,  # 审核状态-用于审核，撤销：2：通过；6：不通过；6：撤销
    "transferStatus": 0,  # 汇款状态-用于汇款成功，汇款失败：4：汇款成功，5：汇款失败。
    "walletWithdrawId": 0,  # 余额提现id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_auditWithdraw(data=data, headers=headers):
    """
    余额提现审批-审核
    /mgmt/fin/wallet/auditWithdraw

    参数说明:
    - auditRemark: 审批备注
    - remittanceRemark: 汇款备注
    - status: 审核状态-用于审核，撤销：2：通过；6：不通过；6：撤销
    - transferStatus: 汇款状态-用于汇款成功，汇款失败：4：汇款成功，5：汇款失败。
    - walletWithdrawId: 余额提现id
    """

    url = "/mgmt/fin/wallet/auditWithdraw"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
