import os

from util.client import client

data = {
    "account": "",  # 付款账号
    "bankName": "",  # 付款银行
    "changeReason": "",  # 调整原因
    "companyCode": "",  # 分公司code
    "inputMan": "",  # 录入人
    "receiptAccount": "",  # 收款账号
    "receiptBankName": "",  # 收款银行
    "remark": "",  # 备注
    "remitMoney": 0.0,  # 款项金额
    "sourceType": 0,  # 款项类型 7->手工退押货款、8->手工增押货款、9->转销售、 14->钱包款与押货款互转、12-其它  19->押货保证金转移
    "sourceTypeName": "",  # 款项类型 手工退押货款、手工增押货款、转销售、钱包款与押货款互转、其它 、押货保证金转移
    "storeCode": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_addManualInputRemit(data=data, headers=headers):
    """
    手工录入流水
    /mgmt/inventory/remit/addManualInputRemit

    参数说明:
    - account: 付款账号
    - bankName: 付款银行
    - changeReason: 调整原因
    - companyCode: 分公司code
    - inputMan: 录入人
    - receiptAccount: 收款账号
    - receiptBankName: 收款银行
    - remark: 备注
    - remitMoney: 款项金额
    - sourceType: 款项类型 7->手工退押货款、8->手工增押货款、9->转销售、 14->钱包款与押货款互转、12-其它  19->押货保证金转移
    - sourceTypeName: 款项类型 手工退押货款、手工增押货款、转销售、钱包款与押货款互转、其它 、押货保证金转移
    """

    url = "/mgmt/inventory/remit/addManualInputRemit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
