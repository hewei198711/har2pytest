import os

from util.client import client

data = {
    "attachmentList": [],  # 附件列表(销售小票)
    "batchNumber": "",  # 生产批号
    "buyDate": "",  # 购买日期 #格式yyyy-MM-dd
    "cardNo": "",  # 顾客卡号
    "contact": "",  # 手机号码
    "custAddress": "",  # 顾客地址
    "customerId": 0,  # 顾客ID
    "failReasonId": 0,  # 故障原因id(后台配置)
    "failureDate": "",  # 故障日期 #格式yyyy-MM-dd
    "failureReason": "",  # 故障原因
    "orderNo": "",  # 订单号
    "produceDate": "",  # 生产日期 #格式yyyy-MM-dd
    "productCode": "",  # 产品编号
    "productName": "",  # 产品名称
    "quantity": 0,  # 申请数量
    "realname": "",  # 顾客姓名
    "reasonDetail": "",  # 故障详细描述
    "scope": 0,  # 整/部件损坏情况：1->整件；2->部件
    "serialNo": "",  # 序列号/二维码
    "shelfLife": 0,  # 保质期属性：1->保质期内；2->保质期外
    "storeCode": "",  # 服务中心编号
    "systemCode": 0,  # 查询系统编码
    "useDate": "",  # 使用日期 #格式yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_addFactoryOrder(data=data, headers=headers):
    """
    新增返厂维修单
    /mgmt/order/factory/addFactoryOrder

    参数说明:
    - attachmentList: 附件列表(销售小票)
    - batchNumber: 生产批号
    - buyDate: 购买日期 #格式yyyy-MM-dd
    - cardNo: 顾客卡号
    - contact: 手机号码
    - custAddress: 顾客地址
    - customerId: 顾客ID
    - failReasonId: 故障原因id(后台配置)
    - failureDate: 故障日期 #格式yyyy-MM-dd
    - failureReason: 故障原因
    - orderNo: 订单号
    - produceDate: 生产日期 #格式yyyy-MM-dd
    - productCode: 产品编号
    - productName: 产品名称
    - quantity: 申请数量
    - realname: 顾客姓名
    - reasonDetail: 故障详细描述
    - scope: 整/部件损坏情况：1->整件；2->部件
    - serialNo: 序列号/二维码
    - shelfLife: 保质期属性：1->保质期内；2->保质期外
    - storeCode: 服务中心编号
    - systemCode: 查询系统编码
    - useDate: 使用日期 #格式yyyy-MM-dd
    """

    url = "/mgmt/order/factory/addFactoryOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
