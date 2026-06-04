import os

from util.client import client

data = {
    "backImageZone": {"backgroundColor": "", "bottomImgUrl": "", "topImgUrl": ""},  # 背景图片配置
    "commitType": 0,  # 提交类型: 1:保存; 2:发布
    "displayTarget": "",  # 发布展示对象: 1:会员; 2:VIP会员; 3:云商; 4:微店; 7:游客(多选使用逗号分隔)
    "id": 0,  # id (编辑时必传)
    "isPreViewCommit": 0,  # 是否预览提交: 1:预览提交; 0:普通提交
    "items": [
        {
            "adminModuleCon": [],
            "adminModuleConTemp": {},
            "foldThreshold": 0,
            "imageNavType": "",
            "isFold": 0,
            "moduleCon": [
                {
                    "heightPer": 0.0,
                    "hotArea": [
                        {
                            "heightPer": 0.0,
                            "leftPer": 0.0,
                            "linkParam": {
                                "linkType": 0,
                                "productList": [{"serialNo": "", "sort": 0}],
                                "promotion": {
                                    "activityType": 0,
                                    "content": "",
                                    "detailImg": "",
                                    "isSetBg": 0,
                                    "listImg": "",
                                    "promotionId": 0,
                                    "promotionType": 0,
                                    "promotionTypeExt": 0,
                                },
                                "targetValue": "",
                                "targetValueExt": "",
                                "targetValueExt2": "",
                            },
                            "topPer": 0.0,
                            "widthPer": 0.0,
                        }
                    ],
                    "imgUrl": "",
                    "isHotArea": 0,
                    "leftPer": 0.0,
                    "linkParam": {
                        "linkType": 0,
                        "productList": [{"serialNo": "", "sort": 0}],
                        "promotion": {
                            "activityType": 0,
                            "content": "",
                            "detailImg": "",
                            "isSetBg": 0,
                            "listImg": "",
                            "promotionId": 0,
                            "promotionType": 0,
                            "promotionTypeExt": 0,
                        },
                        "targetValue": "",
                        "targetValueExt": "",
                        "targetValueExt2": "",
                    },
                    "name": "",
                    "topPer": 0.0,
                    "widthPer": 0.0,
                }
            ],
            "moduleConTemp": {
                "heightPer": 0.0,
                "hotArea": [
                    {
                        "heightPer": 0.0,
                        "leftPer": 0.0,
                        "linkParam": {
                            "linkType": 0,
                            "productList": [{"serialNo": "", "sort": 0}],
                            "promotion": {
                                "activityType": 0,
                                "content": "",
                                "detailImg": "",
                                "isSetBg": 0,
                                "listImg": "",
                                "promotionId": 0,
                                "promotionType": 0,
                                "promotionTypeExt": 0,
                            },
                            "targetValue": "",
                            "targetValueExt": "",
                            "targetValueExt2": "",
                        },
                        "topPer": 0.0,
                        "widthPer": 0.0,
                    }
                ],
                "imgUrl": "",
                "isHotArea": 0,
                "leftPer": 0.0,
                "linkParam": {
                    "linkType": 0,
                    "productList": [{"serialNo": "", "sort": 0}],
                    "promotion": {
                        "activityType": 0,
                        "content": "",
                        "detailImg": "",
                        "isSetBg": 0,
                        "listImg": "",
                        "promotionId": 0,
                        "promotionType": 0,
                        "promotionTypeExt": 0,
                    },
                    "targetValue": "",
                    "targetValueExt": "",
                    "targetValueExt2": "",
                },
                "name": "",
                "topPer": 0.0,
                "widthPer": 0.0,
            },
            "moduleType": 0,
            "pictStyleOne": 0,
            "pictStyleThree": 0,
            "pictStyleTwo": 0,
            "styleType": 0,
        }
    ],  # 模块列表
    "location": 0,  # 端口(显示位置): 2:APP; 3:小程序
    "shelfConfig": 0,  # 上下架配置: 1:立即发布; 2:定时发布; 3:定时上下架
    "shelfOffTime": "",  # 定时下架时间
    "shelfUpTime": "",  # 定时发布时间
    "templateName": "",  # 首页模板名称
    "versionCode": "",  # 版本编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_addHomePage(data=data, headers=headers):
    """
    新增魔法首页
    /mgmt/cms/magicHomePage/addHomePage

    参数说明:
    - backImageZone: 背景图片配置
    - backImageZone.backgroundColor: 背景图颜色
    - backImageZone.bottomImgUrl: 底部背景图
    - backImageZone.topImgUrl: 顶部背景图
    - commitType: 提交类型: 1:保存; 2:发布
    - displayTarget: 发布展示对象: 1:会员; 2:VIP会员; 3:云商; 4:微店; 7:游客(多选使用逗号分隔)
    - id: id (编辑时必传)
    - isPreViewCommit: 是否预览提交: 1:预览提交; 0:普通提交
    - items: 模块列表
    - items.adminModuleCon: 前端编辑缓存
    - items.adminModuleConTemp: 图片导航-图片广告编辑缓存
    - items.foldThreshold: 折叠数量门槛
    - items.imageNavType: 图片导航组件 1.图片导航 2.图片广告
    - items.isFold: 是否折叠：0.否 1.是
    - items.moduleCon: 模块内容
    - items.moduleCon.heightPer: 高边距
    - items.moduleCon.hotArea: 热区列表
    - items.moduleCon.hotArea.heightPer: 高边距
    - items.moduleCon.hotArea.leftPer: 左边距
    - items.moduleCon.hotArea.linkParam: 关联信息
    - items.moduleCon.hotArea.linkParam.linkType: 关联类型:0.不做任何操作 1.关联商品列表 2.关联商品详情页 3.关联活动 4.商城内部链接 5.外部链接 6.问卷 7.抽奖活动 8.签约购活动2.0 9.随心购活动列表 10.随心购活动详情 11.一级分类 14.签约购活动3.0 15.S+S+S活动 16.签约购4.0落地页 17.跳转其他小程序
    - items.moduleCon.hotArea.linkParam.productList: 关联产品编码列表
    - items.moduleCon.hotArea.linkParam.productList.serialNo: 产品编码
    - items.moduleCon.hotArea.linkParam.productList.sort: sort
    - items.moduleCon.hotArea.linkParam.promotion: 关联活动信息
    - items.moduleCon.hotArea.linkParam.promotion.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - items.moduleCon.hotArea.linkParam.promotion.content: 活动列表内容
    - items.moduleCon.hotArea.linkParam.promotion.detailImg: 活动详情背景图
    - items.moduleCon.hotArea.linkParam.promotion.isSetBg: 是否设置背景图，0：否；1:是
    - items.moduleCon.hotArea.linkParam.promotion.listImg: 活动列表背景图
    - items.moduleCon.hotArea.linkParam.promotion.promotionId: 活动ID
    - items.moduleCon.hotArea.linkParam.promotion.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - items.moduleCon.hotArea.linkParam.promotion.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - items.moduleCon.hotArea.linkParam.targetValue: 所有单值的关联内容(主键):抽奖/随心购活动id、商品详情页商品编码、问卷key、内外部链接、一级分类id、对应的模块id
    - items.moduleCon.hotArea.linkParam.targetValueExt: 关联内容补充(appId、一级分类名称)、活动类型
    - items.moduleCon.hotArea.linkParam.targetValueExt2: 关联内容补充2
    - items.moduleCon.hotArea.topPer: 顶部边距
    - items.moduleCon.hotArea.widthPer: 宽边距
    - items.moduleCon.imgUrl: 图片地址
    - items.moduleCon.isHotArea: 是否热区: 0.否 1.是
    - items.moduleCon.leftPer: 左边距
    - items.moduleCon.linkParam: 关联信息
    - items.moduleCon.linkParam.linkType: 关联类型:0.不做任何操作 1.关联商品列表 2.关联商品详情页 3.关联活动 4.商城内部链接 5.外部链接 6.问卷 7.抽奖活动 8.签约购活动2.0 9.随心购活动列表 10.随心购活动详情 11.一级分类 14.签约购活动3.0 15.S+S+S活动 16.签约购4.0落地页 17.跳转其他小程序
    - items.moduleCon.linkParam.productList: 关联产品编码列表
    - items.moduleCon.linkParam.productList.serialNo: 产品编码
    - items.moduleCon.linkParam.productList.sort: sort
    - items.moduleCon.linkParam.promotion: 关联活动信息
    - items.moduleCon.linkParam.promotion.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - items.moduleCon.linkParam.promotion.content: 活动列表内容
    - items.moduleCon.linkParam.promotion.detailImg: 活动详情背景图
    - items.moduleCon.linkParam.promotion.isSetBg: 是否设置背景图，0：否；1:是
    - items.moduleCon.linkParam.promotion.listImg: 活动列表背景图
    - items.moduleCon.linkParam.promotion.promotionId: 活动ID
    - items.moduleCon.linkParam.promotion.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - items.moduleCon.linkParam.promotion.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - items.moduleCon.linkParam.targetValue: 所有单值的关联内容(主键):抽奖/随心购活动id、商品详情页商品编码、问卷key、内外部链接、一级分类id、对应的模块id
    - items.moduleCon.linkParam.targetValueExt: 关联内容补充(appId、一级分类名称)、活动类型
    - items.moduleCon.linkParam.targetValueExt2: 关联内容补充2
    - items.moduleCon.name: 名称
    - items.moduleCon.topPer: 顶部边距
    - items.moduleCon.widthPer: 宽边距
    - items.moduleConTemp: 图片导航-图片广告编辑缓存
    - items.moduleConTemp.heightPer: 高边距
    - items.moduleConTemp.hotArea: 热区列表
    - items.moduleConTemp.hotArea.heightPer: 高边距
    - items.moduleConTemp.hotArea.leftPer: 左边距
    - items.moduleConTemp.hotArea.linkParam: 关联信息
    - items.moduleConTemp.hotArea.linkParam.linkType: 关联类型:0.不做任何操作 1.关联商品列表 2.关联商品详情页 3.关联活动 4.商城内部链接 5.外部链接 6.问卷 7.抽奖活动 8.签约购活动2.0 9.随心购活动列表 10.随心购活动详情 11.一级分类 14.签约购活动3.0 15.S+S+S活动 16.签约购4.0落地页 17.跳转其他小程序
    - items.moduleConTemp.hotArea.linkParam.productList: 关联产品编码列表
    - items.moduleConTemp.hotArea.linkParam.productList.serialNo: 产品编码
    - items.moduleConTemp.hotArea.linkParam.productList.sort: sort
    - items.moduleConTemp.hotArea.linkParam.promotion: 关联活动信息
    - items.moduleConTemp.hotArea.linkParam.promotion.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - items.moduleConTemp.hotArea.linkParam.promotion.content: 活动列表内容
    - items.moduleConTemp.hotArea.linkParam.promotion.detailImg: 活动详情背景图
    - items.moduleConTemp.hotArea.linkParam.promotion.isSetBg: 是否设置背景图，0：否；1:是
    - items.moduleConTemp.hotArea.linkParam.promotion.listImg: 活动列表背景图
    - items.moduleConTemp.hotArea.linkParam.promotion.promotionId: 活动ID
    - items.moduleConTemp.hotArea.linkParam.promotion.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - items.moduleConTemp.hotArea.linkParam.promotion.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - items.moduleConTemp.hotArea.linkParam.targetValue: 所有单值的关联内容(主键):抽奖/随心购活动id、商品详情页商品编码、问卷key、内外部链接、一级分类id、对应的模块id
    - items.moduleConTemp.hotArea.linkParam.targetValueExt: 关联内容补充(appId、一级分类名称)、活动类型
    - items.moduleConTemp.hotArea.linkParam.targetValueExt2: 关联内容补充2
    - items.moduleConTemp.hotArea.topPer: 顶部边距
    - items.moduleConTemp.hotArea.widthPer: 宽边距
    - items.moduleConTemp.imgUrl: 图片地址
    - items.moduleConTemp.isHotArea: 是否热区: 0.否 1.是
    - items.moduleConTemp.leftPer: 左边距
    - items.moduleConTemp.linkParam: 关联信息
    - items.moduleConTemp.linkParam.linkType: 关联类型:0.不做任何操作 1.关联商品列表 2.关联商品详情页 3.关联活动 4.商城内部链接 5.外部链接 6.问卷 7.抽奖活动 8.签约购活动2.0 9.随心购活动列表 10.随心购活动详情 11.一级分类 14.签约购活动3.0 15.S+S+S活动 16.签约购4.0落地页 17.跳转其他小程序
    - items.moduleConTemp.linkParam.productList: 关联产品编码列表
    - items.moduleConTemp.linkParam.productList.serialNo: 产品编码
    - items.moduleConTemp.linkParam.productList.sort: sort
    - items.moduleConTemp.linkParam.promotion: 关联活动信息
    - items.moduleConTemp.linkParam.promotion.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - items.moduleConTemp.linkParam.promotion.content: 活动列表内容
    - items.moduleConTemp.linkParam.promotion.detailImg: 活动详情背景图
    - items.moduleConTemp.linkParam.promotion.isSetBg: 是否设置背景图，0：否；1:是
    - items.moduleConTemp.linkParam.promotion.listImg: 活动列表背景图
    - items.moduleConTemp.linkParam.promotion.promotionId: 活动ID
    - items.moduleConTemp.linkParam.promotion.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - items.moduleConTemp.linkParam.promotion.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - items.moduleConTemp.linkParam.targetValue: 所有单值的关联内容(主键):抽奖/随心购活动id、商品详情页商品编码、问卷key、内外部链接、一级分类id、对应的模块id
    - items.moduleConTemp.linkParam.targetValueExt: 关联内容补充(appId、一级分类名称)、活动类型
    - items.moduleConTemp.linkParam.targetValueExt2: 关联内容补充2
    - items.moduleConTemp.name: 名称
    - items.moduleConTemp.topPer: 顶部边距
    - items.moduleConTemp.widthPer: 宽边距
    - items.moduleType: 模块类型: 0.文字导航; 1.图片广告; 2.图片导航; 3.活动专区; 4.楼层页; 5.魔方; 6.推荐产品;
    - items.pictStyleOne: 图片样式1: 1.直角 2.圆角
    - items.pictStyleThree: 图片样式3: 1.顶边 2.不顶边
    - items.pictStyleTwo: 图片样式2: 1.无白边 2.有白边
    - items.styleType: 展示类型: 0.一行一个 1.一行两个 2.大图模式 3.一大两小 4.横向滑动 5.轮播图海报 6.一行四个 7.一行五个
    - location: 端口(显示位置): 2:APP; 3:小程序
    - shelfConfig: 上下架配置: 1:立即发布; 2:定时发布; 3:定时上下架
    - shelfOffTime: 定时下架时间
    - shelfUpTime: 定时发布时间
    - templateName: 首页模板名称
    - versionCode: 版本编号
    """

    url = "/mgmt/cms/magicHomePage/addHomePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
