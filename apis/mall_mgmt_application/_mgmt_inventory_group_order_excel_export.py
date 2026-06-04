import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "consigneeMobile": "",  # 收货人电话
    "consigneeName": "",  # 收货人姓名
    "createBegin": 0,  # 下单开始时间
    "createEnd": 0,  # 下单结束时间
    "institution": "",  # 团购单位
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "principalCardNo": "",  # 负责人会员卡号
    "principalName": "",  # 服务中心负责人(顾客)姓名
    "state": 0,  # 状态
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_excel_export(params=params, headers=headers):
    """
    导出团购单
    /mgmt/inventory/group-order/excel-export

    参数说明:
    - companyCode: 分公司编号
    - consigneeMobile: 收货人电话
    - consigneeName: 收货人姓名
    - createBegin: 下单开始时间
    - createEnd: 下单结束时间
    - institution: 团购单位
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 页大小
    - principalCardNo: 负责人会员卡号
    - principalName: 服务中心负责人(顾客)姓名
    - state: 状态
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/inventory/group-order/excel-export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
