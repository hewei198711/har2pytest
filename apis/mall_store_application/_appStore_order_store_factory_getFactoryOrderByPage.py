import os

from util.client import client

params = {
    "cardNo": "",  # 顾客卡号
    "companyCodes": [],  # 分公司编号
    "contact": "",  # 顾客联系电话
    "createBeginTime": "",  # 申请开始时间 #格式yyyy-MM-dd
    "createEndTime": "",  # 申请结束时间 #格式yyyy-MM-dd
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "productInfo": "",  # 产品信息
    "realName": "",  # 顾客姓名
    "repairNo": "",  # 返修单单号
    "repairStatus": 0,  # 返厂维修单状态：1->待审核 2->待退回 3->待检测 4->待付费 5->待回寄 6->待收货  97->已取消  98->已驳回 99->已完成
    "storeCode": "",  # 服务中心编号
    "systemCode": 0,  # 查询系统编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_store_factory_getFactoryOrderByPage(params=params, headers=headers):
    """
    分页获取返厂维修单
    /appStore/order/store/factory/getFactoryOrderByPage

    参数说明:
    - cardNo: 顾客卡号
    - companyCodes: 分公司编号
    - contact: 顾客联系电话
    - createBeginTime: 申请开始时间 #格式yyyy-MM-dd
    - createEndTime: 申请结束时间 #格式yyyy-MM-dd
    - pageNum: 页数
    - pageSize: 每页显示数
    - productInfo: 产品信息
    - realName: 顾客姓名
    - repairNo: 返修单单号
    - repairStatus: 返厂维修单状态：1->待审核 2->待退回 3->待检测 4->待付费 5->待回寄 6->待收货  97->已取消  98->已驳回 99->已完成
    - storeCode: 服务中心编号
    - systemCode: 查询系统编码
    """

    url = "/appStore/order/store/factory/getFactoryOrderByPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
