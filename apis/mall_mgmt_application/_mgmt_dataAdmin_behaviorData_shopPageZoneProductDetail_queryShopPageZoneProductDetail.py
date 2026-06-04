import os

from util.client import client

data = {
    "baId": 0,  # 行为数据分析总表id
    "endTime": "",  # 结束时间
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "platformName": "",  # 平台名称 APP 、PC、WEIXIN_PROGRAM
    "startTime": "",  # 开始时间
    "zoneActionType": "",  # 专区商品购买类型 10、产品加购车 20、产品立即购买、30 产品提交订单
    "zoneId": 0,  # 专区id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_shopPageZoneProductDetail_queryShopPageZoneProductDetail(data=data, headers=headers):
    """
    专区页查询产品加购、立即购买、提交订单
    /mgmt/dataAdmin/behaviorData/shopPageZoneProductDetail/queryShopPageZoneProductDetail

    参数说明:
    - baId: 行为数据分析总表id
    - endTime: 结束时间
    - platformName: 平台名称 APP 、PC、WEIXIN_PROGRAM
    - startTime: 开始时间
    - zoneActionType: 专区商品购买类型 10、产品加购车 20、产品立即购买、30 产品提交订单
    - zoneId: 专区id
    """

    url = "/mgmt/dataAdmin/behaviorData/shopPageZoneProductDetail/queryShopPageZoneProductDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
