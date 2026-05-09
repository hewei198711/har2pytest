import os

from util.client import client

params = {
    "bizType": 0,  # 来源：1押货 2押货退回 3交付数量 4交付退回 5库存调整
    "createBegin": "",  # 开始时间
    "createEnd": "",  # 结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码或产品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_details_in_export_excel(params=params, headers=headers):
    """
    导出入库明细
    /appStore/dis-inventory/details/in/export-excel

    参数说明:
    - bizType: 来源：1押货 2押货退回 3交付数量 4交付退回 5库存调整
    - createBegin: 开始时间
    - createEnd: 结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码或产品名称
    """

    url = "/appStore/dis-inventory/details/in/export-excel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
