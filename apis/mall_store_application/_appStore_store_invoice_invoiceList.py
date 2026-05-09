import os

from util.client import client

data = {
    "chargeType": "",  # 费用类型，0:配送费；2:服务费。(不传查全部)
    "collectionCompanyName": "",  # 收款单位名称（支持模糊查询）
    "createTime": "",  # 发票采集日期，YYYY-MM-DD~YYYY-MM-DD
    "expressNo": "",  # 快递单号
    "from": 0,  # TODO: 添加参数说明
    "invoiceCode": "",  # 发票代码
    "invoiceDate": "",  # 开票日期，YYYY-MM-DD~YYYY-MM-DD
    "invoiceNoBegin": "",  # 发票起始号码
    "invoiceNoEnd": "",  # 发票结束号码
    "invoiceType": "",  # 发票类型【枚举同新增发票接口】
    "memberNo": "",  # 会员卡号，应用层不用传
    "memberType": 0,  # 会员类型，应用层不用传
    "month": "",  # 月份，YYYY.MM。不传查全部
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payerCompanyName": "",  # 付款单位名称（支持模糊查询）
    "progress": "",  # 发票进度已签收、未签收。不传查全部
    "reimbursementType": 0,  # 报销类型：1：配送费-分公司，2：配送费-总公司，3：服务费-总公司，4：服务费-扬州，不传查全部
    "serviceCentreNo": "",  # 服务中心/公司编号，应用层不用传
    "storeCode": "",  # 服务中心编号，应用层不用传
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceList(data=data, headers=headers):
    """
    发票采集记录列表
    /appStore/store/invoice/invoiceList

    参数说明:
    - chargeType: 费用类型，0:配送费；2:服务费。(不传查全部)
    - collectionCompanyName: 收款单位名称（支持模糊查询）
    - createTime: 发票采集日期，YYYY-MM-DD~YYYY-MM-DD
    - expressNo: 快递单号
    - invoiceCode: 发票代码
    - invoiceDate: 开票日期，YYYY-MM-DD~YYYY-MM-DD
    - invoiceNoBegin: 发票起始号码
    - invoiceNoEnd: 发票结束号码
    - invoiceType: 发票类型【枚举同新增发票接口】
    - memberNo: 会员卡号，应用层不用传
    - memberType: 会员类型，应用层不用传
    - month: 月份，YYYY.MM。不传查全部
    - pageNum: 页数
    - pageSize: 每页显示数
    - payerCompanyName: 付款单位名称（支持模糊查询）
    - progress: 发票进度已签收、未签收。不传查全部
    - reimbursementType: 报销类型：1：配送费-分公司，2：配送费-总公司，3：服务费-总公司，4：服务费-扬州，不传查全部
    - serviceCentreNo: 服务中心/公司编号，应用层不用传
    - storeCode: 服务中心编号，应用层不用传
    """

    url = "/appStore/store/invoice/invoiceList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
