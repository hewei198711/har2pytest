import os

from util.client import client

data = {
    "activityPrice": "",  # 活动价
    "appContent": "",  # app富文本内容
    "attrs": "",  # 商品属性 json
    "batDistTime": 0,  # 待开启押货分配时间
    "batDistType": 0,  # 开启押货分配类型 1-定时，2-立即
    "batReturnEndTime": 0,  # 押货退货期-结束时间
    "batReturnStartTime": 0,  # 押货退货期-开始时间
    "boxNum": 0,  # 装箱数量
    "brandId": "",  # 品牌id
    "brandTitle": "",  # 品牌名
    "bundleProducts": [{"amount": 0, "subId": "", "subVerId": ""}],  # 组合商品
    "buyNoticeChannel": 0,  # 购买提示渠道 0-空, 1-押货,99-全选
    "buyNoticeContent": "",  # 购买提示内容
    "catalogId": "",  # 类型id
    "catalogTitle": "",  # 类型名
    "customProducts": [{"cusSerialNo": "", "cusTitle": ""}],  # 定制商品
    "customerCardTypes": [],  # 会员卡限购类型 1-未开卡,2-未升级,3-待激活,4-有效 5-已失效
    "customerIdentityTypes": [],  # 身份限购类型  1-普通顾客,2-优惠顾客,3-云商,4-微店
    "deliverWay": 0,  # 交付方式 0-空, 1-公司交付,2-门店交付,99-全选
    "depositDiscountPrice": "",  # 定金优惠金额
    "directSale": 0,  # 是否直销，1-是，0-否
    "discountBoxNum": 0,  # 85折装箱数量
    "discountPrice": "",  # 折扣价
    "discussCopy": "",  # 评论文案
    "distTime": 0,  # 待开启销售分配时间
    "distType": 0,  # 开启销售分配类型 1-定时，2-立即
    "downSaleTime": 0,  # 待下架时间
    "energyDesc": "",  # 能量文案
    "energyNum": "",  # 能量值
    "energyTitle": "",  # 能量名称
    "giftEndTime": 0,  # 礼品-结束时间
    "giftStartTime": 0,  # 礼品-开始时间
    "groupPrice": "",  # 团购价
    "guarantee": "",  # 保质期
    "id": "",  # 商品版本id，新建版本时为空
    "introduction": "",  # 产品简介
    "isActivateItem": 0,  # 是否升级商品 1-是，0-否
    "isBatDist": 0,  # 开启押货分配 1-是，0-否
    "isBuyNotice": 0,  # 是否购买提示 1是 0否
    "isCompanyProduce": 0,  # 是否本/母/控股公司生产，1-是，0-否
    "isConsumeStock": 0,  # 是否消耗服务中心库存 1-是，0否
    "isDeliver": 0,  # 是否发货 1-是，0-否
    "isDist": 0,  # 开启销售分配 1-是，0-否
    "isExchangeProduct": 0,  # 是否换购商品 1-是，0-否
    "isGift": 0,  # 是否礼品，1-是，0-否
    "isGiftBox": 0,  # 是否礼盒，1-是，0-否
    "isHide": 0,  # 是否隐藏 1-是，0-否
    "isIdentityLimit": 0,  # 是否身份限购 1-是，0-否
    "isInstall": 0,  # 是否支持安装 1-是，0-否
    "isInvoice": 0,  # 是否开发票 1-是，0-否
    "isJinhua": 0,  # 是否精华，1-是，0-否
    "isLimitNum": 0,  # 是否产品限购  1-是，0-否
    "isOneOrder": 0,  # 是否支持单独下单 1-是，0-否
    "isPreProduct": 0,  # 是否预售产品 1-是，0-否
    "isProductReturn": 0,  # 是否支持可申请退货 1-是，0-否
    "isProxybuyHide": 0,  # 是否代购隐藏产品，1-是，0-否
    "isRepair": 0,  # 是否支持维修 1-是，0-否
    "isReturnRepair": 0,  # isReturnRepair 是否支持返厂维修 1-是，0-否
    "isShowPilu": 0,  # 是否展示到披露网，1-是，0-否
    "isSignProduct": 0,  # 是否签约购产品 1-是，0-否
    "isStopBat": 0,  # 是否停止押货 1-是，0-否
    "isStopDiscountBat": 0,  # 是否禁止85折押货 1-是，0-否
    "isStopDiscountTransfer": 0,  # 是否禁止85折转分 1-是，0-否
    "isStopSale": 0,  # 是否停止销售 1-是，0-否
    "isTopShow": 0,  # 是否置顶展示 1-是，0-否
    "isUseCoupon": 0,  # 是否必须用优惠券，1-是，0-否
    "isWelfareBuy": 0,  # 是否公益购产品，1-是，0-否
    "lclFeeId": "",  # 85折拼箱费模板id
    "lclFeeTpl": "",  # 85折拼箱费模板名
    "marketTime": 0,  # 上市时间
    "meterUnit": "",  # 计量单位
    "offSaleTime": 0,  # 下架时间时间戳
    "onSaleTime": 0,  # 上架时间时间戳
    "orderPrice": "",  # 85折押货价
    "orderPriceA": "",  # 分级押货价A等-65
    "orderPriceB": "",  # 分级押货价B等-70
    "orderPriceC": "",  # 分级押货价C等-75
    "orderPriceD": "",  # 分级押货价D等-85
    "orderType": 0,  # 订单类型，1-产品订货，2-资料订货，3-订制品订货, 4-赠品领取, 5-配件订货
    "orderWay": 0,  # 下单方式 0-空, 1-自购,2-代购,99-全选
    "packing": "",  # 包装规格
    "preDepositPrice": "",  # 预售定金
    "processMode": 0,  # 加工方式，1-自制，2-外购
    "productId": "",  # 商品id，新建版本时为空
    "productType": 0,  # 商品类型 1-商品，2-定制商品，3-组合商品
    "propertyRights": "",  # 产权
    "purchaseLimitNum": 0,  # 限购数量
    "purchaseLimitType": 0,  # 限购类型， 1-终身限购 2-每月限购
    "purchaseMinNum": 0,  # 起购数量
    "purchaseMinType": 0,  # 起购类型 0-不限起购 1-限制起购
    "pv": "",  # 积分
    "relProducts": [{"relProductId": "", "relSerialNo": ""}],  # 关联产品集合
    "retailPrice": "",  # 零售价
    "saleCompanyId": "",  # 销售主体id
    "saleCompanyTitle": "",  # 销售主体名
    "saleTimeType": 0,  # 上下架类型，1立即上架 2立即下架 3定时上架 4定时下架 5定时上下架
    "securityPrice": "",  # 1:3押货价
    "serialNo": "",  # 商品编码
    "serveContent": "",  # 服务说明
    "shareCopy": "",  # 分享文案
    "shippingId": "",  # 运费模板id
    "shippingTpl": "",  # 运费模板名
    "showIds": [],  # 前端标签id
    "slogan": "",  # 宣传标语
    "stockStatus": 0,  # 库存状态:1库存充足2库存紧张3暂时缺货4即将售罄
    "stopBatTime": 0,  # 待停止押货时间
    "stopBatType": 0,  # 停止押货类型 1-定时，2-立即
    "stopDiscountBatTime": 0,  # 待停止85折押货时间
    "stopDiscountBatType": 0,  # 停止85折押货类型 1-定时，2-立即
    "stopDiscountTransferEndTime": 0,  # 待停止85折转分结束时间
    "stopDiscountTransferTime": 0,  # 待停止85折转分开始时间
    "stopDiscountTransferType": 0,  # 停止85折转分类型 1-定时，2-立即, 3-定时开始与结束
    "tags": [],  # 标签id
    "title": "",  # 商品名称
    "trademarkTitle": "",  # 商标产品名称
    "upSaleTime": 0,  # 待上架时间
    "useCouponId": "",  # 用券时优惠券id
    "verMedais": [{"mediaType": 0, "sort": 0, "storageType": 0, "url": ""}],  # 媒体信息
    "version": "",  # 版本编码
    "versionStatus": 0,  # 状态：1-草稿，2-待产品审核
    "webContent": "",  # web富文本内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
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
    - bundleProducts.amount: 子商品数量
    - bundleProducts.subId: 子商品id
    - bundleProducts.subVerId: 子商品版本id
    - buyNoticeChannel: 购买提示渠道 0-空, 1-押货,99-全选
    - buyNoticeContent: 购买提示内容
    - catalogId: 类型id
    - catalogTitle: 类型名
    - customProducts: 定制商品
    - customProducts.cusSerialNo: 二级编码
    - customProducts.cusTitle: 定制名称
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
    - relProducts.relProductId: 关联商品id
    - relProducts.relSerialNo: 关联商品编码
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
    - verMedais.mediaType: 媒体类型，1-图片 2-视频
    - verMedais.sort: 排序
    - verMedais.storageType: 存储类型，1-FastDFS
    - verMedais.url: 图片、视频地址
    - version: 版本编码
    - versionStatus: 状态：1-草稿，2-待产品审核
    - webContent: web富文本内容
    """

    url = "/mgmt/product/item/saveVersion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
