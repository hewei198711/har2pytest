import os

from util.client import client

data = {
    "companyCode": "",  # 分公司code
    "companyName": "",  # 分公司名称
    "inputMan": "",  # 录入备注
    "inputRemark": "",  # 录入备注
    "payAccount": "",  # 付款账号
    "payAccountBankName": "",  # 付款银行名称
    "receiptAccount": "",  # 收款账号
    "receiptBankName": "",  # 收款银行名称
    "remitMoney": 0.0,  # 款项金额
    "sourceType": 0,  # 款项类型  3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移、24-> 转销售
    "storeCode": "",  # 店铺编号
    "storeName": "",  # 店铺名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManualInputRemit_add(data=data, headers=headers):
    """
    85折手工录入流水
    /mgmt/inventory/disManualInputRemit/add

    参数说明:
    - companyCode: 分公司code
    - companyName: 分公司名称
    - inputMan: 录入备注
    - inputRemark: 录入备注
    - payAccount: 付款账号
    - payAccountBankName: 付款银行名称
    - receiptAccount: 收款账号
    - receiptBankName: 收款银行名称
    - remitMoney: 款项金额
    - sourceType: 款项类型  3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移、24-> 转销售
    - storeCode: 店铺编号
    - storeName: 店铺名称
    """

    url = "/mgmt/inventory/disManualInputRemit/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
