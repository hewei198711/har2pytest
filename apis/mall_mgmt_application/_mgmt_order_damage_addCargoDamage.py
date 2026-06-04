import os

from util.client import client

data = {
    "customerCard": "",  # 顾客卡号
    "customerName": "",  # 顾客姓名
    "damageAmountTotal": 0.0,  # 货损/货差金额合计
    "damageGoods": [{"name": "", "url": ""}],  # 货物清单最多上传3张
    "damageNumTotal": 0,  # 货损/货差数量合计
    "damageOthers": [{"name": "", "url": ""}],  # 其他凭证,最多上传3张
    "damagePhotos": [{"name": "", "url": ""}],  # 货损照片,最多上传3张
    "damageRemarks": "",  # 备注
    "damageType": 0,  # 货损货差类型 1货损 2货差
    "orderNo": "",  # 关联订单号
    "productList": [
        {"damageAmount": 0.0, "damageDetail": "", "damageDetailId": "", "damageNum": 0, "productCode": ""}
    ],  # 货损货差商品列表
    "receiveTime": "",  # 收货时间 #格式yyyy-MM-dd HH:mm:ss
    "sixSidesPhotos": [{"name": "", "url": ""}],  # 外箱六个面照片,最多上传6张
    "source": 0,  # 申请端口 : 1=油葱商城 ,2=运营后台
    "storeCode": "",  # 服务中心编号
    "systemCode": 0,  # 操作编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_damage_addCargoDamage(data=data, headers=headers):
    """
    后台新建货损货差
    /mgmt/order/damage/addCargoDamage

    参数说明:
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - damageAmountTotal: 货损/货差金额合计
    - damageGoods: 货物清单最多上传3张
    - damageGoods.name: 文件名称
    - damageGoods.url: 文件url
    - damageNumTotal: 货损/货差数量合计
    - damageOthers: 其他凭证,最多上传3张
    - damageOthers.name: 文件名称
    - damageOthers.url: 文件url
    - damagePhotos: 货损照片,最多上传3张
    - damagePhotos.name: 文件名称
    - damagePhotos.url: 文件url
    - damageRemarks: 备注
    - damageType: 货损货差类型 1货损 2货差
    - orderNo: 关联订单号
    - productList: 货损货差商品列表
    - productList.damageAmount: 金额小计
    - productList.damageDetail: 详情描述
    - productList.damageDetailId: 详情描述id
    - productList.damageNum: 货损/货差数量
    - productList.productCode: 商品编码
    - receiveTime: 收货时间 #格式yyyy-MM-dd HH:mm:ss
    - sixSidesPhotos: 外箱六个面照片,最多上传6张
    - sixSidesPhotos.name: 文件名称
    - sixSidesPhotos.url: 文件url
    - source: 申请端口 : 1=油葱商城 ,2=运营后台
    - storeCode: 服务中心编号
    - systemCode: 操作编码
    """

    url = "/mgmt/order/damage/addCargoDamage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
