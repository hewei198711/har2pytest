import os

from util.client import client

params = {
    "changeEndDate": "",  # 经营模式切换结束日期 yyyy-MM-dd
    "changeStartDate": "",  # 经营模式切换开始日期 yyyy-MM-dd
    "companyCode": [],  # 分公司code
    "inventoryIsZero": 0,  # 库存是否为0:  0为0 1不为0
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "settleAccount": 0,  # 结清账户 0未结清 1已结清
    "shopType": 0,  # 网点类型
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryTransfer_export(params=params, headers=headers):
    """
    导出押货转移管理列表
    /mgmt/inventory/disInventoryTransfer/export

    参数说明:
    - changeEndDate: 经营模式切换结束日期 yyyy-MM-dd
    - changeStartDate: 经营模式切换开始日期 yyyy-MM-dd
    - companyCode: 分公司code
    - inventoryIsZero: 库存是否为0:  0为0 1不为0
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - settleAccount: 结清账户 0未结清 1已结清
    - shopType: 网点类型
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/inventory/disInventoryTransfer/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
