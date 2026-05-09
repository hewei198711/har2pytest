import os

from util.client import client

data = {
    "amountPayable": 0.0,  # 可领取金额
    "cardNo": "",  # 会员卡号
    "detailDtoList": [],  # TODO: 添加参数说明
    "expressCompany": "",  # 快递公司
    "expressNo": "",  # 快递单号
    "feeType": 0,  # 费用类型（0配送费，2服务费）
    "invoiceQuantity": 0,  # 发票张数
    "invoiceTotalAmount": 0.0,  # 发票总金额
    "mailingAddress": "",  # 邮寄地址
    "memberName": "",  # 会员姓名
    "packageId": 0,  # 发票包Id,新增不传，修改时必传
    "paymentCompanyName": "",  # 付款单位名称
    "paymentCompanyNo": "",  # 付款单位编号
    "recipientName": "",  # 收票人
    "shopCode": "",  # 服务中心编号
    "shopName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_confirmCommit(data=data, headers=headers):
    """
    确认申请
    /appStore/store/invoice/confirmCommit

    参数说明:
    - amountPayable: 可领取金额
    - cardNo: 会员卡号
    - expressCompany: 快递公司
    - expressNo: 快递单号
    - feeType: 费用类型（0配送费，2服务费）
    - invoiceQuantity: 发票张数
    - invoiceTotalAmount: 发票总金额
    - mailingAddress: 邮寄地址
    - memberName: 会员姓名
    - packageId: 发票包Id,新增不传，修改时必传
    - paymentCompanyName: 付款单位名称
    - paymentCompanyNo: 付款单位编号
    - recipientName: 收票人
    - shopCode: 服务中心编号
    - shopName: 服务中心名称
    """

    url = "/appStore/store/invoice/confirmCommit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
