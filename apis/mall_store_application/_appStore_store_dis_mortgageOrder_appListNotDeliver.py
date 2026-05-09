import os

from util.client import client

params = {
    "endTime": "",  # 结束提交时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 商品编号
    "startTime": "",  # 开始提交时间
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_appListNotDeliver(params=params, headers=headers):
    """
    APP欠货未发列表查询
    /appStore/store/dis/mortgageOrder/appListNotDeliver

    参数说明:
    - endTime: 结束提交时间
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 商品编号
    - startTime: 开始提交时间
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/dis/mortgageOrder/appListNotDeliver"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
