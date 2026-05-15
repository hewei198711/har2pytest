import os

from util.client import client

data = {
    "amountPayable": 0.0,  # 可领取金额
    "cardNo": "",  # 会员卡号
    "detailDtoList": [
        {
            "agreementStatus": 0,
            "amount": 0.0,
            "checkCode": "",
            "checkStatus": 0,
            "checkStatusCode": "",
            "collectionCompany": "",
            "collectionCompanyCode": "",
            "id": 0,
            "invoiceCode": "",
            "invoiceDate": "",
            "invoiceNumber": "",
            "invoiceNumberEnd": "",
            "invoiceType": 0,
            "invoiceUrl": "",
            "taxFreeAmount": 0.0,
        }
    ],  # TODO: 添加参数说明
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
    - detailDtoList.agreementStatus: 合作协议签署状态：0未签署1已签署。传1
    - detailDtoList.amount: 发票含税金额
    - detailDtoList.checkCode: 校验码（后6位）
    - detailDtoList.checkStatus: 验票结果状态0未验票1成功2失败
    - detailDtoList.checkStatusCode: 验票结果状态码
    - detailDtoList.collectionCompany: 收款单位名称
    - detailDtoList.collectionCompanyCode: 收款单位编号
    - detailDtoList.id: 发票主键Id，新增不传，修改时必传
    - detailDtoList.invoiceCode: 发票代码
    - detailDtoList.invoiceDate: 开票日期
    - detailDtoList.invoiceNumber: 发票号码起
    - detailDtoList.invoiceNumberEnd: 发票号码止
    - detailDtoList.invoiceType: 发票类型，1：增值税普通发票； 2：增值税电子普通发票；3：增值税普通发票（卷式）；4：通用机打发票；5：通用机打（电子）发票；6：通用手工发票；7：通用定额发票；8：增值税专用发票；9：增值税电子专用发票；10：全电普票
    - detailDtoList.invoiceUrl: 发票Url
    - detailDtoList.taxFreeAmount: 不含税金额
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
