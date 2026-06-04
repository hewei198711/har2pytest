import os

from util.client import client

params = {
    "downloadType": 0,  # 下载途径，1：运营后台，2：门店系统
    "endDownloadDate": "",  # 结束下载时间(yyyy-MM-dd HH:mm)
    "id": 0,  # id
    "operator": "",  # 下载人
    "producedAddress": 0,  # 产地:1中山基地;2扬州基地;3吉林基地;4淮北基地
    "productCode": "",  # 产品代码
    "productName": "",  # 成品名称
    "productNumber": "",  # 批号
    "startDownloadDate": "",  # 开始下载时间(yyyy-MM-dd HH:mm)
    "storeCode": "",  # 下载服务中心
    "storeName": "",  # 下载服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportManage_exportProductReportDownloadLog(params=params, headers=headers):
    """
    成品报告下载日志导出
    /mgmt/store/productReportManage/exportProductReportDownloadLog

    参数说明:
    - downloadType: 下载途径，1：运营后台，2：门店系统
    - endDownloadDate: 结束下载时间(yyyy-MM-dd HH:mm)
    - id: id
    - operator: 下载人
    - producedAddress: 产地:1中山基地;2扬州基地;3吉林基地;4淮北基地
    - productCode: 产品代码
    - productName: 成品名称
    - productNumber: 批号
    - startDownloadDate: 开始下载时间(yyyy-MM-dd HH:mm)
    - storeCode: 下载服务中心
    - storeName: 下载服务中心名称
    """

    url = "/mgmt/store/productReportManage/exportProductReportDownloadLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
