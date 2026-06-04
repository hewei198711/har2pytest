import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编码
    "companyName": "",  # 分公司
    "customerCard": "",  # 顾客卡号
    "exchangeNo": "",  # 换货单号
    "exchangeType": 0,  # 换货类型：1->顾客换货 2->押货换货
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "pickupMonth": "",  # 月份 yyyy-MM
    "storeCode": "",  # 服务中心编号
    "waybillNo": "",  # 快递单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_as_sfDifferentExport(params=params, headers=headers):
    """
    上门取件差异表导出
    /mgmt/order/as/sfDifferentExport

    参数说明:
    - companyCode: 分公司编码
    - companyName: 分公司
    - customerCard: 顾客卡号
    - exchangeNo: 换货单号
    - exchangeType: 换货类型：1->顾客换货 2->押货换货
    - pageNum: 页数
    - pageSize: 每页显示数
    - pickupMonth: 月份 yyyy-MM
    - storeCode: 服务中心编号
    - waybillNo: 快递单号
    """

    url = "/mgmt/order/as/sfDifferentExport"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
