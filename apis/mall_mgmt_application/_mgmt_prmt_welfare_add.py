import os

from util.client import client

data = {
    "customOneName": "",  # 自定义属性一名称(目标捐款金额)
    "customOneValue": 0,  # 自定义属性一值
    "customTwoName": "",  # 自定义属性二名称(每100能量对应的捐款金额)
    "customTwoValue": 0.0,  # 自定义属性二值
    "endTime": "",  # 结束时间
    "id": 0,  # 主键id
    "modules": [
        {
            "advertPictures": [{"linkType": 0, "linkValue": "", "picture": "", "sort": 0}],
            "advertStyleOne": 0,
            "advertStyleTwo": 0,
            "floorProducts": [{"serialNo": "", "sort": 0}],
            "foldThreshold": 0,
            "isFold": False,
            "moduleName": "",
            "poolContent": "",
            "poolDisplay": False,
            "sort": 0,
            "styleType": 0,
            "textRemark": "",
            "textRemarkBackgroundColor": "",
            "title": "",
            "type": 0,
            "videoPictureUrl": "",
            "videoUrl": "",
        }
    ],  # 模块集合
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "pushMessage": False,  # 账单推送开关 true-开启 false-关闭
    "startTime": "",  # 开始时间
    "storeTarget": 0,  # 门店目标能量值
    "themeBackgroundColor": "",  # 主题页背景色
    "themeName": "",  # 活动页名称
    "wxSharePicture": "",  # 小程序分享卡片图片地址
    "wxShareRemark": "",  # 小程序分享卡片文案
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_welfare_add(data=data, headers=headers):
    """
    新建活动
    /mgmt/prmt/welfare/add

    参数说明:
    - customOneName: 自定义属性一名称(目标捐款金额)
    - customOneValue: 自定义属性一值
    - customTwoName: 自定义属性二名称(每100能量对应的捐款金额)
    - customTwoValue: 自定义属性二值
    - endTime: 结束时间
    - id: 主键id
    - modules: 模块集合
    - modules.advertPictures: 图片广告-图片信息集合
    - modules.advertPictures.linkType: 广告图片关联类型(0-不跳转，1-专区页面，2-商品详情)
    - modules.advertPictures.linkValue: 关联值(专区id/商品编码)
    - modules.advertPictures.picture: 广告图片地址
    - modules.advertPictures.sort: 广告图片排序
    - modules.advertStyleOne: 图片广告样式1 (1-直角 2-圆角)
    - modules.advertStyleTwo: 图片广告样式2 (1.无白边 2.有白边)
    - modules.floorProducts: 楼层页-商品信息集合
    - modules.floorProducts.serialNo: 商品编码
    - modules.floorProducts.sort: 商品排序
    - modules.foldThreshold: 楼层页商品折叠数量
    - modules.isFold: 楼层页商品是否折叠:true-不折叠 false-折叠
    - modules.moduleName: 模块名称
    - modules.poolContent: 爱心池提示语
    - modules.poolDisplay: 爱心池进度条是否显示 true-显示 false-隐藏
    - modules.sort: 模块排序
    - modules.styleType: 展示方式/列表样式: (0.一行一个 1.一行两个 2.大图模式 3.一大两小 4.横向滑动 5.轮播图海报)
    - modules.textRemark: 富文本文字
    - modules.textRemarkBackgroundColor: 富文本背景色
    - modules.title: 楼层页标题
    - modules.type: 模块类型(1-图片广告，2-楼层页，3-文本，4-视频，5-爱心守护池)
    - modules.videoPictureUrl: 视频封面图片地址
    - modules.videoUrl: 视频地址
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - pushMessage: 账单推送开关 true-开启 false-关闭
    - startTime: 开始时间
    - storeTarget: 门店目标能量值
    - themeBackgroundColor: 主题页背景色
    - themeName: 活动页名称
    - wxSharePicture: 小程序分享卡片图片地址
    - wxShareRemark: 小程序分享卡片文案
    """

    url = "/mgmt/prmt/welfare/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
