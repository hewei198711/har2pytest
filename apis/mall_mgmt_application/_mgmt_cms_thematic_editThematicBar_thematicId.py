import os

from util.client import client

params = {
    "thematicId": 0,  # thematicId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_thematic_editThematicBar_thematicId(params=params, headers=headers):
    """
    编辑专题页
    /mgmt/cms/thematic/editThematicBar/{thematicId}

    参数说明:
    - activityId: 关联的活动id(签约购、随心购)
    - decorationPromotionReqVo: 关联活动信息
    - decorationPromotionReqVo.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - decorationPromotionReqVo.content: 活动列表内容
    - decorationPromotionReqVo.detailImg: 活动详情背景图
    - decorationPromotionReqVo.isSetBg: 是否设置背景图，0：否；1:是
    - decorationPromotionReqVo.listImg: 活动列表背景图
    - decorationPromotionReqVo.promotionId: 活动ID
    - decorationPromotionReqVo.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - decorationPromotionReqVo.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - descript: 专题描述
    - name: 专题菜单名称
    - productList: 关联产品编码列表
    - productList.serialNo: 产品编码
    - productList.sort: sort
    - relateType: 关联类型,1:关联产品; 2:关联活动; 4:签约购活动2.0; 5:关联随心购活动; 6:随心购活动列表; 7.专区页面; 8.签约购活动3.0; 9.S+S+S活动; 10.签约购4.0落地页 11.送礼活动;
    - sort: 排序
    - targetValue: 关联的内容值
    - thematicId: thematicId
    """

    url = f"/mgmt/cms/thematic/editThematicBar/{params['thematicId']}"
    with client.get(url=url, headers=headers) as r:
        return r
