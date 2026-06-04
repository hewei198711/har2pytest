import os

from util.client import client

data = {
    "auditRemark": "",  # 审批备注
    "auditStatus": 0,  # 审核结果:1：待审核；2：已通过；3：已驳回；7：待提交
    "creditEffectTime": "",  # 信用额生效时间
    "walletCreditApplyIdList": [],  # 顾客信用额申请id集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_submitApply(data=data, headers=headers):
    """
    顾客信用额列表-提交审核
    /mgmt/fin/wallet/credit/submitApply

    参数说明:
    - auditRemark: 审批备注
    - auditStatus: 审核结果:1：待审核；2：已通过；3：已驳回；7：待提交
    - creditEffectTime: 信用额生效时间
    - walletCreditApplyIdList: 顾客信用额申请id集合
    """

    url = "/mgmt/fin/wallet/credit/submitApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
