import os

from util.client import client

data = {
    "authLicense": {"fileName": "", "url": ""},  # 授权委托书
    "bankAccount": "",  # 开户银行账号
    "bankLicense": {"fileName": "", "url": ""},  # 银行开户许可证
    "bankName": "",  # 开户银行名称
    "bizLicense": {"fileName": "", "url": ""},  # 营业执照副本
    "draweeName": "",  # 单位名称/个人姓名
    "invoiceUrls": [],  # 发票地址
    "orderNo": "",  # 团购单编号
    "phone": "",  # 联系电话
    "registerAddress": "",  # 注册地址
    "registerPhone": "",  # 注册电话
    "state": 0,  # 开票状态 1->未开票 2->已开票 3->已退票
    "taxpayerNo": "",  # 纳税人识别号
    "type": 0,  # 开票类型 1->个人普通电子票 2->企业普通电子发票 3->企业专用纸质发票(增值税专用电子发票)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_invoice_apply(data=data, headers=headers):
    """
    团购单申请开发票
    /mgmt/inventory/group-order/invoice/apply

    参数说明:
    - authLicense: 授权委托书
    - authLicense.fileName: 文件名称
    - authLicense.url: 文件地址
    - bankAccount: 开户银行账号
    - bankLicense: 银行开户许可证
    - bankLicense.fileName: 文件名称
    - bankLicense.url: 文件地址
    - bankName: 开户银行名称
    - bizLicense: 营业执照副本
    - bizLicense.fileName: 文件名称
    - bizLicense.url: 文件地址
    - draweeName: 单位名称/个人姓名
    - invoiceUrls: 发票地址
    - orderNo: 团购单编号
    - phone: 联系电话
    - registerAddress: 注册地址
    - registerPhone: 注册电话
    - state: 开票状态 1->未开票 2->已开票 3->已退票
    - taxpayerNo: 纳税人识别号
    - type: 开票类型 1->个人普通电子票 2->企业普通电子发票 3->企业专用纸质发票(增值税专用电子发票)
    """

    url = "/mgmt/inventory/group-order/invoice/apply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
