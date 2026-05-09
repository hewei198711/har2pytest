import os

from util.client import client

data = {
    "attachmentList": [],  # 附件列表(销售小票)
    "batchNum": "",  # 生产批号
    "buyDate": "",  # 购买日期 #格式yyyy-MM-dd
    "custAddress": "",  # 顾客地址
    "custCard": "",  # 顾客卡号
    "customer": "",  # 顾客姓名
    "failDate": "",  # 故障日期 #格式yyyy-MM-dd
    "failReason": "",  # 故障原因
    "failReasonId": 0,  # 故障原因id(后台配置)
    "orderNo": "",  # 关联订单号
    "phoneNum": "",  # 联系电话
    "produceDate": "",  # 生产日期 #格式yyyy-MM-dd
    "productCode": "",  # 产品编号
    "productName": "",  # 产品名称
    "quantity": 0,  # 申请数量
    "reasonDetail": "",  # 原因详细描述
    "scope": 0,  # 维修范围：1->整件；2->部件
    "serialNo": "",  # 序列号/二维码
    "shelfLife": 0,  # 保质期属性：1->保质期内 2->保质期外
    "storeCode": "",  # 服务中心编号
    "systemCode": 0,  # 操作系统编码
    "useDate": "",  # 使用日期 #格式yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_order_repair_add(data=data, headers=headers):
    """
    新增维修单
    /appStore/mobile/order/repair/add

    参数说明:
    - attachmentList: 附件列表(销售小票)
    - batchNum: 生产批号
    - buyDate: 购买日期 #格式yyyy-MM-dd
    - custAddress: 顾客地址
    - custCard: 顾客卡号
    - customer: 顾客姓名
    - failDate: 故障日期 #格式yyyy-MM-dd
    - failReason: 故障原因
    - failReasonId: 故障原因id(后台配置)
    - orderNo: 关联订单号
    - phoneNum: 联系电话
    - produceDate: 生产日期 #格式yyyy-MM-dd
    - productCode: 产品编号
    - productName: 产品名称
    - quantity: 申请数量
    - reasonDetail: 原因详细描述
    - scope: 维修范围：1->整件；2->部件
    - serialNo: 序列号/二维码
    - shelfLife: 保质期属性：1->保质期内 2->保质期外
    - storeCode: 服务中心编号
    - systemCode: 操作系统编码
    - useDate: 使用日期 #格式yyyy-MM-dd
    """

    url = "/appStore/mobile/order/repair/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
