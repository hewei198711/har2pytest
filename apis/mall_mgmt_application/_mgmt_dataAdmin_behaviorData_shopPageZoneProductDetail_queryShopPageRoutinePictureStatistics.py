import os

from util.client import client

data = {
    "baId": 0,  # 行为数据分析总表id
    "endTime": "",  # 结束时间
    "homePagePictureId": 0,  # 首页icon图片id
    "operateTimeType": "",  # 时间查询条件 按月传 'operateMonth'、按天传'operateDay'、按小时传 'operateHour' 查询类型
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "pictureId": 0,  # 图标、图片id
    "platformName": "",  # 平台名称 APP 、PC、WEIXIN_PROGRAM
    "slideShowPictureId": 0,  # 轮播图图片id
    "startTime": "",  # 开始时间
    "topicPagePictureId": 0,  # 专题页图片id
    "zoneId": 0,  # 专区id [10、图片广告数据明细，11、图片导航书明细 按需传专区id值(例如：丽玲专区id)]
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_shopPageZoneProductDetail_queryShopPageRoutinePictureStatistics(
    data=data, headers=headers
):
    """
    查询[常规]数据看板图片统计相关接口
    /mgmt/dataAdmin/behaviorData/shopPageZoneProductDetail/queryShopPageRoutinePictureStatistics

    参数说明:
    - baId: 行为数据分析总表id
    - endTime: 结束时间
    - homePagePictureId: 首页icon图片id
    - operateTimeType: 时间查询条件 按月传 'operateMonth'、按天传'operateDay'、按小时传 'operateHour' 查询类型
    - pictureId: 图标、图片id
    - platformName: 平台名称 APP 、PC、WEIXIN_PROGRAM
    - slideShowPictureId: 轮播图图片id
    - startTime: 开始时间
    - topicPagePictureId: 专题页图片id
    - zoneId: 专区id [10、图片广告数据明细，11、图片导航书明细 按需传专区id值(例如：丽玲专区id)]
    """

    url = "/mgmt/dataAdmin/behaviorData/shopPageZoneProductDetail/queryShopPageRoutinePictureStatistics"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
