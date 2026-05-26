import os

from util.client import client

data = {
    "id": "",  # 商品版本id，新建版本时为空
    "productType": 1,  # 商品类型 1-商品，2-定制商品，3-组合商品
    "productId": "",  # 商品id，新建版本时为空
    "versionStatus": 2,  # 状态：1-草稿，2-待产品审核
    "serialNo": "ZP052101",  # 商品编码
    "discountBoxNum": None,  # 85折装箱数量
    "catalogTitle": "健康食品",  # 类型名
    "catalogId": "5",  # 类型id
    "showIds": ["5"],  # 前端标签id
    "isShowPilu": 0,  # 是否展示到披露网，1-是，0-否
    "isCompanyProduce": 1,  # 是否本/母/控股公司生产，1-是，0-否
    "marketTime": "",  # 上市时间
    "title": "赠赠一号",  # 商品名称
    "brandTitle": "完美",  # 品牌名
    "brandId": "2",  # 品牌id
    "meterUnit": "",  # 计量单位
    "slogan": "",  # 宣传标语
    "energyTitle": "",  # 能量名称
    "energyDesc": "",  # 能量文案
    "packing": "",  # 包装规格
    "boxNum": "",  # 装箱数量
    "saleCompanyTitle": "完美中国",  # 销售主体名
    "saleCompanyId": "2",  # 销售主体id
    "propertyRights": "",  # 产权
    "processMode": "",  # 加工方式，1-自制，2-外购
    "orderType": 4,  # 订单类型，1-产品订货，2-资料订货，3-订制品订货, 4-赠品领取, 5-配件订货
    "shippingTpl": "按订单金额收取运费",  # 运费模板名
    "shippingId": "1217978678543324234",  # 运费模板id
    "directSale": 0,  # 是否直销，1-是，0-否
    "stockStatus": None,  # 库存状态:1库存充足2库存紧张3暂时缺货4即将售罄
    "guarantee": "",  # 保质期
    "tags": [],  # 标签id
    "bundleProducts": [],  # 组合商品
    "relProducts": [],  # 关联产品集合
    "customProducts": [],  # 定制商品
    "lclFeeId": "",  # 85折拼箱费模板id
    "retailPrice": 0,  # 零售价
    "securityPrice": 0,  # 1:3押货价
    "groupPrice": 0,  # 团购价
    "pv": 0,  # 积分
    "orderPrice": 0,  # 85折押货价
    "orderPriceA": 0,  # 分级押货价A等-65
    "orderPriceB": 0,  # 分级押货价B等-70
    "orderPriceC": 0,  # 分级押货价C等-75
    "orderPriceD": 0,  # 分级押货价D等-85
    "activityPrice": 0,  # 活动价
    "preDepositPrice": 0,  # 预售定金
    "depositDiscountPrice": 0,  # 定金优惠金额
    "discountPrice": "",  # 折扣价
    "attrs": "{}",  # 商品属性 json
    "verMedais": [
        {
            "mediaType": 1,
            "sort": 1,
            "storageType": 1,
            "url": "https://ucoss-test.perfect99.com/mall-center-product/20260521140818h6E1i.png",
        }
    ],  # 媒体信息
    "videoMedais": [],  # TODO: 添加参数说明
    "imgMedais": [
        {
            "mediaType": 1,
            "sort": 1,
            "storageType": 1,
            "url": "https://ucoss-test.perfect99.com/mall-center-product/20260521140818h6E1i.png",
        }
    ],  # TODO: 添加参数说明
    "webContent": "",  # web富文本内容
    "appContent": "",  # app富文本内容
    "serveContent": "",  # 服务说明
    "shareCopy": "",  # 分享文案
    "discussCopy": "",  # 评论文案
    "introduction": "",  # 产品简介
    "stopBatType": 2,  # 停止押货类型 1-定时，2-立即
    "batDistType": None,  # 开启押货分配类型 1-定时，2-立即
    "distType": None,  # 开启销售分配类型 1-定时，2-立即
    "stopBatTime": None,  # 待停止押货时间
    "batDistTime": None,  # 待开启押货分配时间
    "distTime": None,  # 待开启销售分配时间
    "ExchangeProductTime": None,  # TODO: 添加参数说明
    "stopDiscountBatType": 2,  # 停止85折押货类型 1-定时，2-立即
    "stopDiscountBatTime": None,  # 待停止85折押货时间
    "stopDiscountTransferType": None,  # 停止85折转分类型 1-定时，2-立即, 3-定时开始与结束
    "stopDiscountTransferTime": None,  # 待停止85折转分开始时间
    "stopDiscountTransferEndTime": None,  # 待停止85折转分结束时间
    "isStopBat": 1,  # 是否停止押货 1-是，0-否
    "isBatDist": 0,  # 开启押货分配 1-是，0-否
    "isDist": 0,  # 开启销售分配 1-是，0-否
    "isStopSale": 0,  # 是否停止销售 1-是，0-否
    "isStopDiscountBat": 1,  # 是否禁止85折押货 1-是，0-否
    "isStopDiscountTransfer": 0,  # 是否禁止85折转分 1-是，0-否
    "isExchangeProduct": 0,  # 是否换购商品 1-是，0-否
    "isSignProduct": 0,  # 是否签约购产品 1-是，0-否
    "isHide": 0,  # 是否隐藏 1-是，0-否
    "isProxybuyHide": 0,  # 是否代购隐藏产品，1-是，0-否
    "isWelfareBuy": 0,  # 是否公益购产品，1-是，0-否
    "isJinhua": 0,  # 是否精华，1-是，0-否
    "isGift": 0,  # 是否礼品，1-是，0-否
    "isGiftBox": 0,  # 是否礼盒，1-是，0-否
    "isInstall": 0,  # 是否支持安装 1-是，0-否
    "isBuyNotice": 0,  # 是否购买提示 1是 0否
    "isUseCoupon": 0,  # 是否必须用优惠券，1-是，0-否
    "isTopShow": 0,  # 是否置顶展示 1-是，0-否
    "isRepair": 0,  # 是否支持维修 1-是，0-否
    "isReturnRepair": 0,  # isReturnRepair 是否支持返厂维修 1-是，0-否
    "isConsumeStock": 0,  # 是否消耗服务中心库存 1-是，0否
    "isInvoice": 1,  # 是否开发票 1-是，0-否
    "isOneOrder": 0,  # 是否支持单独下单 1-是，0-否
    "isProductReturn": 1,  # 是否支持可申请退货 1-是，0-否
    "isDeliver": 1,  # 是否发货 1-是，0-否
    "isActivateItem": 0,  # 是否升级商品 1-是，0-否
    "isPreProduct": 0,  # 是否预售产品 1-是，0-否
    "isIdentityLimit": 0,  # 是否身份限购 1-是，0-否
    "isLimitNum": 0,  # 是否产品限购  1-是，0-否
    "orderWay": 99,  # 下单方式 0-空, 1-自购,2-代购,99-全选
    "deliverWay": 99,  # 交付方式 0-空, 1-公司交付,2-门店交付,99-全选
    "purchaseMinType": 0,  # 起购类型 0-不限起购 1-限制起购
    "purchaseLimitType": None,  # 限购类型， 1-终身限购 2-每月限购
    "purchaseMinNum": 1,  # 起购数量
    "saleTimeType": 1,  # 上下架类型，1立即上架 2立即下架 3定时上架 4定时下架 5定时上下架
    "upSaleTime": None,  # 待上架时间
    "downSaleTime": None,  # 待下架时间
    "customerIdentityTypes": [],  # 身份限购类型  1-普通顾客,2-优惠顾客,3-云商,4-微店
    "customerCardTypes": [],  # 会员卡限购类型 1-未开卡,2-未升级,3-待激活,4-有效 5-已失效
    "trademarkTitle": "",  # 商标产品名称
    "useCouponId": "",  # 用券时优惠券id
    "batReturnStartTime": "",  # 押货退货期-开始时间
    "batReturnEndTime": "",  # 押货退货期-结束时间
    "giftStartTime": "",  # 礼品-开始时间
    "giftEndTime": "",  # 礼品-结束时间
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_product_item_saveVersion(data=data, headers=headers):
    """
    添加商品
    /mgmt/product/item/saveVersion

    参数说明:
    - activityPrice: 活动价
    - appContent: app富文本内容
    - attrs: 商品属性 json
    - batDistTime: 待开启押货分配时间
    - batDistType: 开启押货分配类型 1-定时，2-立即
    - batReturnEndTime: 押货退货期-结束时间
    - batReturnStartTime: 押货退货期-开始时间
    - boxNum: 装箱数量
    - brandId: 品牌id
    - brandTitle: 品牌名
    - bundleProducts: 组合商品
    - buyNoticeChannel: 购买提示渠道 0-空, 1-押货,99-全选
    - buyNoticeContent: 购买提示内容
    - catalogId: 类型id
    - catalogTitle: 类型名
    - customProducts: 定制商品
    - customerCardTypes: 会员卡限购类型 1-未开卡,2-未升级,3-待激活,4-有效 5-已失效
    - customerIdentityTypes: 身份限购类型  1-普通顾客,2-优惠顾客,3-云商,4-微店
    - deliverWay: 交付方式 0-空, 1-公司交付,2-门店交付,99-全选
    - depositDiscountPrice: 定金优惠金额
    - directSale: 是否直销，1-是，0-否
    - discountBoxNum: 85折装箱数量
    - discountPrice: 折扣价
    - discussCopy: 评论文案
    - distTime: 待开启销售分配时间
    - distType: 开启销售分配类型 1-定时，2-立即
    - downSaleTime: 待下架时间
    - energyDesc: 能量文案
    - energyNum: 能量值
    - energyTitle: 能量名称
    - giftEndTime: 礼品-结束时间
    - giftStartTime: 礼品-开始时间
    - groupPrice: 团购价
    - guarantee: 保质期
    - id: 商品版本id，新建版本时为空
    - introduction: 产品简介
    - isActivateItem: 是否升级商品 1-是，0-否
    - isBatDist: 开启押货分配 1-是，0-否
    - isBuyNotice: 是否购买提示 1是 0否
    - isCompanyProduce: 是否本/母/控股公司生产，1-是，0-否
    - isConsumeStock: 是否消耗服务中心库存 1-是，0否
    - isDeliver: 是否发货 1-是，0-否
    - isDist: 开启销售分配 1-是，0-否
    - isExchangeProduct: 是否换购商品 1-是，0-否
    - isGift: 是否礼品，1-是，0-否
    - isGiftBox: 是否礼盒，1-是，0-否
    - isHide: 是否隐藏 1-是，0-否
    - isIdentityLimit: 是否身份限购 1-是，0-否
    - isInstall: 是否支持安装 1-是，0-否
    - isInvoice: 是否开发票 1-是，0-否
    - isJinhua: 是否精华，1-是，0-否
    - isLimitNum: 是否产品限购  1-是，0-否
    - isOneOrder: 是否支持单独下单 1-是，0-否
    - isPreProduct: 是否预售产品 1-是，0-否
    - isProductReturn: 是否支持可申请退货 1-是，0-否
    - isProxybuyHide: 是否代购隐藏产品，1-是，0-否
    - isRepair: 是否支持维修 1-是，0-否
    - isReturnRepair: isReturnRepair 是否支持返厂维修 1-是，0-否
    - isShowPilu: 是否展示到披露网，1-是，0-否
    - isSignProduct: 是否签约购产品 1-是，0-否
    - isStopBat: 是否停止押货 1-是，0-否
    - isStopDiscountBat: 是否禁止85折押货 1-是，0-否
    - isStopDiscountTransfer: 是否禁止85折转分 1-是，0-否
    - isStopSale: 是否停止销售 1-是，0-否
    - isTopShow: 是否置顶展示 1-是，0-否
    - isUseCoupon: 是否必须用优惠券，1-是，0-否
    - isWelfareBuy: 是否公益购产品，1-是，0-否
    - lclFeeId: 85折拼箱费模板id
    - lclFeeTpl: 85折拼箱费模板名
    - marketTime: 上市时间
    - meterUnit: 计量单位
    - offSaleTime: 下架时间时间戳
    - onSaleTime: 上架时间时间戳
    - orderPrice: 85折押货价
    - orderPriceA: 分级押货价A等-65
    - orderPriceB: 分级押货价B等-70
    - orderPriceC: 分级押货价C等-75
    - orderPriceD: 分级押货价D等-85
    - orderType: 订单类型，1-产品订货，2-资料订货，3-订制品订货, 4-赠品领取, 5-配件订货
    - orderWay: 下单方式 0-空, 1-自购,2-代购,99-全选
    - packing: 包装规格
    - preDepositPrice: 预售定金
    - processMode: 加工方式，1-自制，2-外购
    - productId: 商品id，新建版本时为空
    - productType: 商品类型 1-商品，2-定制商品，3-组合商品
    - propertyRights: 产权
    - purchaseLimitNum: 限购数量
    - purchaseLimitType: 限购类型， 1-终身限购 2-每月限购
    - purchaseMinNum: 起购数量
    - purchaseMinType: 起购类型 0-不限起购 1-限制起购
    - pv: 积分
    - relProducts: 关联产品集合
    - retailPrice: 零售价
    - saleCompanyId: 销售主体id
    - saleCompanyTitle: 销售主体名
    - saleTimeType: 上下架类型，1立即上架 2立即下架 3定时上架 4定时下架 5定时上下架
    - securityPrice: 1:3押货价
    - serialNo: 商品编码
    - serveContent: 服务说明
    - shareCopy: 分享文案
    - shippingId: 运费模板id
    - shippingTpl: 运费模板名
    - showIds: 前端标签id
    - slogan: 宣传标语
    - stockStatus: 库存状态:1库存充足2库存紧张3暂时缺货4即将售罄
    - stopBatTime: 待停止押货时间
    - stopBatType: 停止押货类型 1-定时，2-立即
    - stopDiscountBatTime: 待停止85折押货时间
    - stopDiscountBatType: 停止85折押货类型 1-定时，2-立即
    - stopDiscountTransferEndTime: 待停止85折转分结束时间
    - stopDiscountTransferTime: 待停止85折转分开始时间
    - stopDiscountTransferType: 停止85折转分类型 1-定时，2-立即, 3-定时开始与结束
    - tags: 标签id
    - title: 商品名称
    - trademarkTitle: 商标产品名称
    - upSaleTime: 待上架时间
    - useCouponId: 用券时优惠券id
    - verMedais: 媒体信息
    - version: 版本编码
    - versionStatus: 状态：1-草稿，2-待产品审核
    - webContent: web富文本内容
    """

    url = "/mgmt/product/item/saveVersion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
