import os

from util.client import client

params = {
    "bannerId": 0,  # bannerId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_banner_editBanner_bannerId(params=params, headers=headers):
    """
    修改Banner
    /mgmt/cms/banner/editBanner/{bannerId}

    参数说明:
    - bannerId: bannerId
    - activityCode: 活动ID
    - appId: 跳转的小程序appId
    - bannerName: banner名称
    - decorationPromotionReqVo: 关联活动信息
    - decorationPromotionReqVo.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - decorationPromotionReqVo.content: 活动列表内容
    - decorationPromotionReqVo.detailImg: 活动详情背景图
    - decorationPromotionReqVo.isSetBg: 是否设置背景图，0：否；1:是
    - decorationPromotionReqVo.listImg: 活动列表背景图
    - decorationPromotionReqVo.promotionId: 活动ID
    - decorationPromotionReqVo.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - decorationPromotionReqVo.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - displayObjects: 展示对象,0:默认选择全部; 1:普通顾客; 2:优惠顾客; 3:云商; 4:微店; 7:游客(多选使用逗号分隔)
    - imageUrl: banner图片地址
    - linkUrl: banner图链接地址
    - location: 显示位置，1：PC商城首页，2：APP，3：小程序
    - path: 跳转的小程序落地页链接
    - productList: 关联产品编码列表
    - productList.serialNo: 产品编码
    - productList.sort: sort
    - projectKey: 问卷key
    - relateType: 关联类型,1:关联产品; 2:关联活动,3:商城内部链接,4:跳转其他小程序,5:外部链接,6:问卷,7:抽奖活动,8:签约购活动2.0,9:随心购活动,10:随心购活动列表,11:签约购活动3.0,12:专区页面,13:签约购活动落地页,14.S+S+S活动,15:签约购4.0,16.送礼活动
    - shelfConfig: 上下架配置,1:立即上架; 2:定时上架;3:定时上下架
    - shelfOffTime: banner下架时间
    - shelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    - shelfUpTime: banner上架时间
    - sort: 排序
    - targetValue: 关联的内容值
    - targetValueExt2: 关联内容补充2
    - topbarColor: app顶栏颜色
    """

    url = f"/mgmt/cms/banner/editBanner/{params['bannerId']}"
    with client.get(url=url, headers=headers) as r:
        return r
