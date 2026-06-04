import os

from util.client import client

data = {
    "cardStatuses": [],  # 会员卡状态:-3.未开卡,-2.未升级,-1.待激活,0.有效,1.已失效,2.已注销
    "customerType": 0,  # 顾客类型(1:所有顾客；2:自定义)
    "detailContent": "",  # 产品图文说明
    "downShelfTime": "",  # 待下架时间
    "exchangeNo": "",  # 兑换产品编码
    "exchangeProductId": "",  # 兑换产品id，新建版本时为空
    "exchangeTime": "",  # 开始兑换时间
    "exchangeTimeType": 0,  # 开始兑换时间类型 1-定时开始，2-即时开始
    "exchangeType": 0,  # 兑换产品类型 1-虚拟物品(优惠券)
    "id": "",  # 兑换产品版本id，新建版本时为空
    "jindouPrice": 0,  # 金豆价格
    "limitMemberLevel": False,  # 是否限制顾客等级
    "maxSaleQuota": 0,  # 最大销售库存
    "memberLevels": [],  # 顾客等级:0.新用户,1.一星优惠客户,2.二星优惠客户,3.三星优惠客户,4.四星优惠客户,5.客户代表,6.客户经理,7.中级客户经理,8.客户总监,9.高级客户总监,10.资深客户总监,11.客户总经理
    "memberTypes": [],  # 顾客身份:1-普通顾客，2-优惠顾客，3-云商，4-微店
    "offShelfType": 0,  # 下架方式1定时下架2不自动下架3领取完直接下架
    "onShelfType": 0,  # 上架方式1定时上架2即时上架
    "picUrl": "",  # 图片地址
    "relationValue": "",  # 关联品
    "rightsContent": "",  # 权益说明
    "showOrder": 0,  # 展示顺序
    "stockType": 0,  # 库存类型 1-限量，2-非限量
    "title": "",  # 兑换产品名称
    "upShelfTime": "",  # 待上架时间
    "version": "",  # 版本编码
    "versionStatus": 0,  # 状态：1-草稿，2-待审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_exhangProduct_saveVersion(data=data, headers=headers):
    """
    添加兑换产品
    /mgmt/prmt/rights/exhangProduct/saveVersion

    参数说明:
    - cardStatuses: 会员卡状态:-3.未开卡,-2.未升级,-1.待激活,0.有效,1.已失效,2.已注销
    - customerType: 顾客类型(1:所有顾客；2:自定义)
    - detailContent: 产品图文说明
    - downShelfTime: 待下架时间
    - exchangeNo: 兑换产品编码
    - exchangeProductId: 兑换产品id，新建版本时为空
    - exchangeTime: 开始兑换时间
    - exchangeTimeType: 开始兑换时间类型 1-定时开始，2-即时开始
    - exchangeType: 兑换产品类型 1-虚拟物品(优惠券)
    - id: 兑换产品版本id，新建版本时为空
    - jindouPrice: 金豆价格
    - limitMemberLevel: 是否限制顾客等级
    - maxSaleQuota: 最大销售库存
    - memberLevels: 顾客等级:0.新用户,1.一星优惠客户,2.二星优惠客户,3.三星优惠客户,4.四星优惠客户,5.客户代表,6.客户经理,7.中级客户经理,8.客户总监,9.高级客户总监,10.资深客户总监,11.客户总经理
    - memberTypes: 顾客身份:1-普通顾客，2-优惠顾客，3-云商，4-微店
    - offShelfType: 下架方式1定时下架2不自动下架3领取完直接下架
    - onShelfType: 上架方式1定时上架2即时上架
    - picUrl: 图片地址
    - relationValue: 关联品
    - rightsContent: 权益说明
    - showOrder: 展示顺序
    - stockType: 库存类型 1-限量，2-非限量
    - title: 兑换产品名称
    - upShelfTime: 待上架时间
    - version: 版本编码
    - versionStatus: 状态：1-草稿，2-待审核
    """

    url = "/mgmt/prmt/rights/exhangProduct/saveVersion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
