import os

from util.client import client

params = {
    "iconId": 0,  # iconId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_iconSetting_editIconSetting_iconId(params=params, headers=headers):
    """
    修改Icon
    /mgmt/cms/iconSetting/editIconSetting/{iconId}

    参数说明:
    - iconId: iconId
    - activityId: 关联的活动id(签约购)
    - appId: 跳转的小程序appId
    - categoryId: icon关联的一级分类Id
    - categoryName: icon关联的一级分类名称
    - decorationPromotionReqVo: 关联活动信息
    - decorationPromotionReqVo.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - decorationPromotionReqVo.content: 活动列表内容
    - decorationPromotionReqVo.detailImg: 活动详情背景图
    - decorationPromotionReqVo.isSetBg: 是否设置背景图，0：否；1:是
    - decorationPromotionReqVo.listImg: 活动列表背景图
    - decorationPromotionReqVo.promotionId: 活动ID
    - decorationPromotionReqVo.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - decorationPromotionReqVo.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - iconName: icon名称
    - imageUrl: icon图片地址
    - linkUrl: icon关联的链接地址
    - location: 显示位置,1:APP,2:小程序
    - path: 跳转的小程序落地页链接
    - productList: 关联产品编码列表
    - productList.serialNo: 产品编码
    - productList.sort: sort
    - productSerialNo: icon关联的商品编号
    - relateType: 关联类型: 1:一级分类,2:商城内部链接,3:外部链接,4:关联产品,5:关联活动,6:跳转其他小程序,7:关联产品详情页,8.签约购活动,9.专区页面,10:签约购4.0落地页
    - shelfConfig: 上下架配置,1:立即上架; 2:定时上架;3:定时上下架
    - shelfOffTime: 下架时间
    - shelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    - shelfUpTime: 上架时间
    - sort: 排序
    - targetValue: 关联的内容值
    """

    url = f"/mgmt/cms/iconSetting/editIconSetting/{params['iconId']}"
    with client.get(url=url, headers=headers) as r:
        return r
