import os

from util.client import client

data = {
    "authorizeLicense": "",  # 授权委托书
    "bankAccount": "",  # 开户银行账号
    "bankLicense": "",  # 银行开户许可证
    "bankName": "",  # 开户银行名称
    "businessLicense": "",  # 营业执照副本
    "createTime": "",  # 创建时间
    "id": 0,  # TODO: 添加参数说明
    "invoiceStatus": 0,  # 开票状态 1->待开票 2->开票中 3->已开票 4->开票失败 5->已退票
    "invoiceType": 0,  # 开票类型 1->个人普通电子票 2->企业普通电子发票 3->企业专用纸质发票
    "invoiceUrls": [],  # 电子发票url
    "name": "",  # 单位名称/个人姓名
    "orderInvoiceReturnVos": [
        {"id": 0, "invoiceCode": "", "invoiceNo": "", "invoiceTime": "", "invoiceUrl": "", "orderInvoiceId": 0}
    ],  # 电子发票返回信息
    "orderNo": "",  # 订单编号
    "phone": "",  # 联系人电话
    "registerAddress": "",  # 注册地址
    "registerPhone": "",  # 注册电话
    "taxpayerNo": "",  # 纳税人识别号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_applyInvoice(data=data, headers=headers):
    """
    申请开票
    /mgmt/order/applyInvoice

    参数说明:
    - authorizeLicense: 授权委托书
    - bankAccount: 开户银行账号
    - bankLicense: 银行开户许可证
    - bankName: 开户银行名称
    - businessLicense: 营业执照副本
    - createTime: 创建时间
    - invoiceStatus: 开票状态 1->待开票 2->开票中 3->已开票 4->开票失败 5->已退票
    - invoiceType: 开票类型 1->个人普通电子票 2->企业普通电子发票 3->企业专用纸质发票
    - invoiceUrls: 电子发票url
    - name: 单位名称/个人姓名
    - orderInvoiceReturnVos: 电子发票返回信息
    - orderInvoiceReturnVos.invoiceCode: 发票代码
    - orderInvoiceReturnVos.invoiceNo: 发票号码
    - orderInvoiceReturnVos.invoiceTime: 开票时间
    - orderInvoiceReturnVos.invoiceUrl: 电子发票url
    - orderInvoiceReturnVos.orderInvoiceId: 主表id
    - orderNo: 订单编号
    - phone: 联系人电话
    - registerAddress: 注册地址
    - registerPhone: 注册电话
    - taxpayerNo: 纳税人识别号
    """

    url = "/mgmt/order/applyInvoice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
