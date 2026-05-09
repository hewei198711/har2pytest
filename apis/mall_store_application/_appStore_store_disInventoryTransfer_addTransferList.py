import os

from util.client import client

data = {
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "productNumQuery": 0,  # 传1大于0;0等于0;-1小于0;2不为0;不传为查全部
    "query": "",  # 搜索条件
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disInventoryTransfer_addTransferList(data=data, headers=headers):
    """
    库存列表
    /appStore/store/disInventoryTransfer/addTransferList

    参数说明:
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - productNumQuery: 传1大于0;0等于0;-1小于0;2不为0;不传为查全部
    - query: 搜索条件
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/disInventoryTransfer/addTransferList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
