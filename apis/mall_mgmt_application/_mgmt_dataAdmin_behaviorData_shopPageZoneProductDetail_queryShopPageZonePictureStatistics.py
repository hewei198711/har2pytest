import os

from util.client import client

data = {
    "adsPictureId": 0,  # 图片广告图片id
    "baId": 0,  # 行为数据分析总表id
    "endTime": "",  # 结束时间
    "navPictureId": 0,  # 图片导航图片id
    "operateTimeType": "",  # 时间查询条件 按月传 'operateMonth'、按天传'operateDay'、按小时传 'operateHour' 查询类型
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "pictureId": 0,  # 图标、图片id
    "platformName": "",  # 平台名称 APP 、PC、WEIXIN_PROGRAM
    "startTime": "",  # 开始时间
    "zoneId": 0,  # 专区id [10、图片广告数据明细，11、图片导航书明细 按需传专区id值(例如：丽玲专区id)]
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_shopPageZoneProductDetail_queryShopPageZonePictureStatistics(
    data=data, headers=headers
):
    """
    查询[专区]数据看板图片统计相关接口
    /mgmt/dataAdmin/behaviorData/shopPageZoneProductDetail/queryShopPageZonePictureStatistics

    参数说明:
    - adsPictureId: 图片广告图片id
    - baId: 行为数据分析总表id
    - endTime: 结束时间
    - navPictureId: 图片导航图片id
    - operateTimeType: 时间查询条件 按月传 'operateMonth'、按天传'operateDay'、按小时传 'operateHour' 查询类型
    - pictureId: 图标、图片id
    - platformName: 平台名称 APP 、PC、WEIXIN_PROGRAM
    - startTime: 开始时间
    - zoneId: 专区id [10、图片广告数据明细，11、图片导航书明细 按需传专区id值(例如：丽玲专区id)]
    """

    url = "/mgmt/dataAdmin/behaviorData/shopPageZoneProductDetail/queryShopPageZonePictureStatistics"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
