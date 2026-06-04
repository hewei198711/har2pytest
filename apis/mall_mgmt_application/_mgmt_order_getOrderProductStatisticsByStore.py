import os

from util.client import client

params = {
    "beginOrderMonth": "",  # 开始业绩月份，格式yyyyMM
    "endOrderMonth": "",  # 结束业绩月份，格式yyyyMM
    "orderMonthList": [],  # 业绩月份数组(前端可不传)
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getOrderProductStatisticsByStore(params=params, headers=headers):
    """
    运营后台-各系列产品服务中心列表
    /mgmt/order/getOrderProductStatisticsByStore

    参数说明:
    - beginOrderMonth: 开始业绩月份，格式yyyyMM
    - endOrderMonth: 结束业绩月份，格式yyyyMM
    - orderMonthList: 业绩月份数组(前端可不传)
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    """

    url = "/mgmt/order/getOrderProductStatisticsByStore"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
