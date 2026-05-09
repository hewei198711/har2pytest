import os

from util.client import client

data = {
    "finishEndDate": "",  # 完成时间结束 yyyy-MM-dd
    "finishStartDate": "",  # 完成时间开始 yyyy-MM-dd
    "orderSn": "",  # 85折押货单号
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "status": 0,  # 状态 1已完成 2待支付 3已取消
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disInventoryTransfer_totalMsg(data=data, headers=headers):
    """
    转移的合计信息
    /appStore/store/disInventoryTransfer/totalMsg

    参数说明:
    - finishEndDate: 完成时间结束 yyyy-MM-dd
    - finishStartDate: 完成时间开始 yyyy-MM-dd
    - orderSn: 85折押货单号
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - status: 状态 1已完成 2待支付 3已取消
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/disInventoryTransfer/totalMsg"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
