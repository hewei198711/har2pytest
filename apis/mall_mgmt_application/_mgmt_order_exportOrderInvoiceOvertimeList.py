import os

from util.client import client

params = {
    "endCreateTime": "",  # 发票信息填写结束时间
    "endInvoiceTime": "",  # 商城提交开票申请结束时间
    "endPayTime": "",  # 支付结束时间
    "financeCompanyCode": "",  # 财务分公司编号
    "from": 0,  # TODO: 添加参数说明
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "startCreateTime": "",  # 发票信息填写开始时间
    "startInvoiceTime": "",  # 商城提交开票申请开始时间
    "startPayTime": "",  # 支付开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exportOrderInvoiceOvertimeList(params=params, headers=headers):
    """
    运营后台-导出查询订单开票超时列表
    /mgmt/order/exportOrderInvoiceOvertimeList

    参数说明:
    - endCreateTime: 发票信息填写结束时间
    - endInvoiceTime: 商城提交开票申请结束时间
    - endPayTime: 支付结束时间
    - financeCompanyCode: 财务分公司编号
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - startCreateTime: 发票信息填写开始时间
    - startInvoiceTime: 商城提交开票申请开始时间
    - startPayTime: 支付开始时间
    """

    url = "/mgmt/order/exportOrderInvoiceOvertimeList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
