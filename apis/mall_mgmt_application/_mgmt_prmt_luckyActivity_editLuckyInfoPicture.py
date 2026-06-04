import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "modifyModule": 0,  # 修改模块类型(10-互动中心展示图，11-PC端背景图，12-APP端背景图，13-小程序分享卡片图，15-分享助力小程序分享卡片图)
    "pictureUrl": "",  # 图片地址
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editLuckyInfoPicture(data=data, headers=headers):
    """
    修改抽奖活动详情页面的相关图片 10-互动中心展示图，11-PC端背景图，12-APP端背景图，13-小程序分享卡片图 15-分享助力小程序分享卡片图
    /mgmt/prmt/luckyActivity/editLuckyInfoPicture

    参数说明:
    - activityId: 活动id
    - modifyModule: 修改模块类型(10-互动中心展示图，11-PC端背景图，12-APP端背景图，13-小程序分享卡片图，15-分享助力小程序分享卡片图)
    - pictureUrl: 图片地址
    """

    url = "/mgmt/prmt/luckyActivity/editLuckyInfoPicture"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
