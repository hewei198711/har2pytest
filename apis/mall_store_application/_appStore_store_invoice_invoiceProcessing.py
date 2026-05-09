import os

from util.client import client

data = {
    "cardNo": "",  # TODO: 添加参数说明
    "createTimeEnd": "",  # 起始时间
    "createTimeStart": "",  # 结束时间
    "from": 0,  # TODO: 添加参数说明
    "invoicePurpose": "",  # 费用类型：1服务费，2配送费（不传查全部）
    "memberType": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "serviceCentreNo": "",  # 服务中心/公司编号
    "storeCode": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceProcessing(data=data, headers=headers):
    """
    发票处理进度，查全部
    /appStore/store/invoice/invoiceProcessing

    参数说明:
    - createTimeEnd: 起始时间
    - createTimeStart: 结束时间
    - invoicePurpose: 费用类型：1服务费，2配送费（不传查全部）
    - pageNum: 页数
    - pageSize: 每页显示数
    - serviceCentreNo: 服务中心/公司编号
    """

    url = "/appStore/store/invoice/invoiceProcessing"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
