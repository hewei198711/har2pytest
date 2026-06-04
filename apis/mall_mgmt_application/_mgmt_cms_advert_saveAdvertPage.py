import os

from util.client import client

data = {
    "activityId": 0,  # 关联的抽奖活动ID
    "advertName": "",  # 广告页名称
    "decorationPromotionReqVo": {
        "activityType": 0,
        "content": "",
        "detailImg": "",
        "isSetBg": 0,
        "listImg": "",
        "promotionId": 0,
        "promotionType": 0,
        "promotionTypeExt": 0,
    },  # 关联活动信息
    "id": 0,  # id
    "imageUrl": "",  # 启动页图片
    "linkUrl": "",  # 广告图链接地址
    "productList": [{"serialNo": "", "sort": 0}],  # 关联产品编码列表
    "productSerialNo": "",  # 关联的产品编号
    "relateType": 0,  # 关联类型: 1.关联链接; 2.关联产品列表; 3.关联产品详情; 4.关联专题页; 5.关联小程序直播间; 6:抽奖活动; 7:专区页面; 8.关联内部链接; 9.关联活动 10.关联随心购活动 11.关联S+S+S活动 12.关联签约购活动2.0; 13.关联签约购活动3.0 14.关联签约购活动落地页 15.关联签约购4.0落地页
    "shelfConfig": 0,  # 上下架配置,1:立即上架; 2:定时上架;3:定时上下架
    "shelfOffTime": 0,  # 下架时间
    "shelfUpTime": 0,  # 上架时间
    "stayTime": 0,  # 广告停留的时间
    "targetValue": "",  # 关联的内容值
    "thematicBarId": 0,  # 关联的专题页Id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_advert_saveAdvertPage(data=data, headers=headers):
    """
    新增广告页
    /mgmt/cms/advert/saveAdvertPage

    参数说明:
    - activityId: 关联的抽奖活动ID
    - advertName: 广告页名称
    - decorationPromotionReqVo: 关联活动信息
    - decorationPromotionReqVo.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - decorationPromotionReqVo.content: 活动列表内容
    - decorationPromotionReqVo.detailImg: 活动详情背景图
    - decorationPromotionReqVo.isSetBg: 是否设置背景图，0：否；1:是
    - decorationPromotionReqVo.listImg: 活动列表背景图
    - decorationPromotionReqVo.promotionId: 活动ID
    - decorationPromotionReqVo.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - decorationPromotionReqVo.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - id: id
    - imageUrl: 启动页图片
    - linkUrl: 广告图链接地址
    - productList: 关联产品编码列表
    - productList.serialNo: 产品编码
    - productList.sort: sort
    - productSerialNo: 关联的产品编号
    - relateType: 关联类型: 1.关联链接; 2.关联产品列表; 3.关联产品详情; 4.关联专题页; 5.关联小程序直播间; 6:抽奖活动; 7:专区页面; 8.关联内部链接; 9.关联活动 10.关联随心购活动 11.关联S+S+S活动 12.关联签约购活动2.0; 13.关联签约购活动3.0 14.关联签约购活动落地页 15.关联签约购4.0落地页
    - shelfConfig: 上下架配置,1:立即上架; 2:定时上架;3:定时上下架
    - shelfOffTime: 下架时间
    - shelfUpTime: 上架时间
    - stayTime: 广告停留的时间
    - targetValue: 关联的内容值
    - thematicBarId: 关联的专题页Id
    """

    url = "/mgmt/cms/advert/saveAdvertPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
