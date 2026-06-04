import os

from util.client import client

data = {
    "applyAmount": 0.0,  # 调整新增信用额度
    "cardNo": "",  # 会员卡号
    "creditAmount": 0.0,  # TODO: 添加参数说明
    "creditApplyId": 0,  # 顾客信用额ID，新增不传，修改必传
    "creditEffectTime": "",  # 调整新增时间
    "instalment": 0,  # 是否分期，1：是，0：否
    "instalmentDesc": "",  # 是否分期: 是 | 否
    "isCommit": 0,  # 是否提交审核，1：是，0:否
    "realname": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_updateApply(data=data, headers=headers):
    """
    顾客信用额列表-修改
    /mgmt/fin/wallet/credit/updateApply

    参数说明:
    - applyAmount: 调整新增信用额度
    - cardNo: 会员卡号
    - creditApplyId: 顾客信用额ID，新增不传，修改必传
    - creditEffectTime: 调整新增时间
    - instalment: 是否分期，1：是，0：否
    - instalmentDesc: 是否分期: 是 | 否
    - isCommit: 是否提交审核，1：是，0:否
    """

    url = "/mgmt/fin/wallet/credit/updateApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
