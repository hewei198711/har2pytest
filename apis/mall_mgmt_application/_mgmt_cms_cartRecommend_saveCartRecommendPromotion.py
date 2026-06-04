import os

from util.client import client

data = {
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
    "linkId": "",  # 关联id(回显)
    "linkStr": "",  # 关联文本(回显)
    "linkType": 0,  # 关联类型: 3.关联活动; 4.商城内部链接; 5.外部链接; 6.问卷; 7.抽奖活动; 9.随心购活动列表; 10.随心购活动详情; 13.专区页面; 15.S+S+S活动; 16.签约购4.0落地页;
    "promotionLabelUrl": "",  # 活动标签图片
    "promotionTitle": "",  # 活动标题
    "targetValue": "",  # 所有单值的关联内容：抽奖/随心购活动id、问卷key、内外部链接
    "targetValueExt": "",  # 关联内容补充(appId、活动类型)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cartRecommend_saveCartRecommendPromotion(data=data, headers=headers):
    """
    保存购物车推荐活动
    /mgmt/cms/cartRecommend/saveCartRecommendPromotion

    参数说明:
    - decorationPromotionReqVo: 关联活动信息
    - decorationPromotionReqVo.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - decorationPromotionReqVo.content: 活动列表内容
    - decorationPromotionReqVo.detailImg: 活动详情背景图
    - decorationPromotionReqVo.isSetBg: 是否设置背景图，0：否；1:是
    - decorationPromotionReqVo.listImg: 活动列表背景图
    - decorationPromotionReqVo.promotionId: 活动ID
    - decorationPromotionReqVo.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - decorationPromotionReqVo.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - linkId: 关联id(回显)
    - linkStr: 关联文本(回显)
    - linkType: 关联类型: 3.关联活动; 4.商城内部链接; 5.外部链接; 6.问卷; 7.抽奖活动; 9.随心购活动列表; 10.随心购活动详情; 13.专区页面; 15.S+S+S活动; 16.签约购4.0落地页;
    - promotionLabelUrl: 活动标签图片
    - promotionTitle: 活动标题
    - targetValue: 所有单值的关联内容：抽奖/随心购活动id、问卷key、内外部链接
    - targetValueExt: 关联内容补充(appId、活动类型)
    """

    url = "/mgmt/cms/cartRecommend/saveCartRecommendPromotion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
