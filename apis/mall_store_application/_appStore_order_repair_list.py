import os

from util.client import client

params = {
    "applyTimeBegin": "",  # 申请开始时间 #格式yyyy-MM-dd
    "applyTimeEnd": "",  # 申请结束时间 #格式yyyy-MM-dd
    "companyCodes": [],  # 分公司编号
    "custCard": "",  # 顾客卡号
    "customer": "",  # 顾客姓名
    "orderNo": "",  # 关联订单号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "phoneNum": "",  # 顾客电话
    "productInfo": "",  # 产品编号或名称
    "repairNo": "",  # 维修单单号
    "repairStatus": 0,  # 维修单状态：1->待处理 2->已接单 3->维修中 98>已取消 99>已完成
    "storeCode": "",  # 服务中心编号
    "systemCode": 0,  # 查询系统编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_repair_list(params=params, headers=headers):
    """
    分页查询维修单信息
    /appStore/order/repair/list

    参数说明:
    - applyTimeBegin: 申请开始时间 #格式yyyy-MM-dd
    - applyTimeEnd: 申请结束时间 #格式yyyy-MM-dd
    - companyCodes: 分公司编号
    - custCard: 顾客卡号
    - customer: 顾客姓名
    - orderNo: 关联订单号
    - pageNum: 页数
    - pageSize: 每页显示数
    - phoneNum: 顾客电话
    - productInfo: 产品编号或名称
    - repairNo: 维修单单号
    - repairStatus: 维修单状态：1->待处理 2->已接单 3->维修中 98>已取消 99>已完成
    - storeCode: 服务中心编号
    - systemCode: 查询系统编码
    """

    url = "/appStore/order/repair/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
