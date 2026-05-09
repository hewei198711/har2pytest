import os

from util.client import client

params = {
    "bizNo": "",  # 来源的 业务id （可能是押货id，可能是商城订单id）
    "bizType": 0,  # 来源：1押货 2押货退回 3交付数量 4交付退回
    "createBegin": "",  # 出/入库开始时间
    "createEnd": "",  # 出/入库结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "type": 0,  # 出入库：1入库 2出库
    "产品编码": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_detail(params=params, headers=headers):
    """
    库存明细
    /appStore/dis-inventory/detail

    参数说明:
    - bizNo: 来源的 业务id （可能是押货id，可能是商城订单id）
    - bizType: 来源：1押货 2押货退回 3交付数量 4交付退回
    - createBegin: 出/入库开始时间
    - createEnd: 出/入库结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - type: 出入库：1入库 2出库
    """

    url = "/appStore/dis-inventory/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
