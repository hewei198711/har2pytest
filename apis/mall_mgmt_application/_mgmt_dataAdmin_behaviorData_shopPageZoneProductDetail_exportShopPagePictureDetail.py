import os

from util.client import client

data = {
    "baId": 0,  # 行为数据分析总表id
    "dataType": "",  # 10、图片广告数据明细，11、图片导航书明细，20、专题数据明细，21、轮播图数据明细，22、首页icon数据明细
    "endTime": "",  # 结束时间
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "pictureId": 0,  # 图片id
    "platformName": "",  # 平台名称 APP 、PC、WEIXIN_PROGRAM
    "startTime": "",  # 开始时间
    "zoneId": 0,  # 专区id [10、图片广告数据明细，11、图片导航书明细 按需传专区id值(例如：丽玲专区id)]
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_shopPageZoneProductDetail_exportShopPagePictureDetail(data=data, headers=headers):
    """
    导出[专区]图片广告数据明细、图片导航明细;[常规]专题数据明细、轮播图数据明细、首页icon数据明细;
    /mgmt/dataAdmin/behaviorData/shopPageZoneProductDetail/exportShopPagePictureDetail

    参数说明:
    - baId: 行为数据分析总表id
    - dataType: 10、图片广告数据明细，11、图片导航书明细，20、专题数据明细，21、轮播图数据明细，22、首页icon数据明细
    - endTime: 结束时间
    - pictureId: 图片id
    - platformName: 平台名称 APP 、PC、WEIXIN_PROGRAM
    - startTime: 开始时间
    - zoneId: 专区id [10、图片广告数据明细，11、图片导航书明细 按需传专区id值(例如：丽玲专区id)]
    """

    url = "/mgmt/dataAdmin/behaviorData/shopPageZoneProductDetail/exportShopPagePictureDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
