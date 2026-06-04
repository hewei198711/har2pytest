import os

from util.client import client

data = {
    "adjustAmount": 0.0,  # 录入金额，支持负数，当增加余额时传正数；减少余额时传负数
    "adjustReason": "",  # 修改原因说明
    "companyCode": "",  # 公司编码
    "transMethod": 0,  # 交易类型
    "type": 0,  # 款项类型 1:还欠款;2:补银行流水3:手工退款4:押货款与钱包互转5:其他
    "walletAdjustId": 0,  # 手工录入款项ID，重新提交必填
    "walletId": 0,  # 钱包id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_applyAdjust(data=data, headers=headers):
    """
    手工录入款项审核-提交
    /mgmt/fin/wallet/applyAdjust

    参数说明:
    - adjustAmount: 录入金额，支持负数，当增加余额时传正数；减少余额时传负数
    - adjustReason: 修改原因说明
    - companyCode: 公司编码
    - transMethod: 交易类型
    - type: 款项类型 1:还欠款;2:补银行流水3:手工退款4:押货款与钱包互转5:其他
    - walletAdjustId: 手工录入款项ID，重新提交必填
    - walletId: 钱包id
    """

    url = "/mgmt/fin/wallet/applyAdjust"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
