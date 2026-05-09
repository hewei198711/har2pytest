import os

from util.client import client

data = {
    "openBank": "",  # 开户行
    "openBankBranch": "",  # 开户支行
    "refundAccount": "",  # 退款账户
    "refundAccountName": "",  # 退款账户名
    "refundAmount": 0.0,  # 退款金额
    "refundReason": "",  # 退款原因
    "refundType": 0,  # 退款类型 1->已汇押货款退款 2->汇错账户退款 3-> 1:3已汇押货款退款 4-> 1：3押货余额转分级押货保证金
    "refundVoucher": "",  # 退款凭证  最多3 张  多张逗号隔开
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_refund_submit_apply(data=data, headers=headers):
    """
    退款申请提交
    /appStore/web/store/refund/submit/apply

    参数说明:
    - openBank: 开户行
    - openBankBranch: 开户支行
    - refundAccount: 退款账户
    - refundAccountName: 退款账户名
    - refundAmount: 退款金额
    - refundReason: 退款原因
    - refundType: 退款类型 1->已汇押货款退款 2->汇错账户退款 3-> 1:3已汇押货款退款 4-> 1：3押货余额转分级押货保证金
    - refundVoucher: 退款凭证  最多3 张  多张逗号隔开
    - storeCode: 服务中心编号
    """

    url = "/appStore/web/store/refund/submit/apply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
