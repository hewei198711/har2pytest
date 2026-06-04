import os

from util.client import client

data = {
    "catalogId": "",  # 商品分类Id
    "exact": 0,  # 搜索是否模糊(0模糊,1精确)
    "exactSerialNos": [],  # 精确商品编码
    "isActivateItem": 0,  # 是否升级商品 1-是 0-否
    "isConsumeStock": 0,  # 是否仅消耗服务中心库存 0-否 1-是
    "isExchangeProduct": 0,  # 是否换购商品 0-否 1-是
    "isFilterCusProduct": 0,  # 是否过滤掉定制产品 0-否 1-是，默认为0
    "isPreProduct": 0,  # 是否预售产品 1-是，0-否
    "isSignProduct": 0,  # 是否签约购产品 1-是，0-否
    "isStopSale": 0,  # 是否停止销售呈报 0-否 1-是
    "orderType": 0,  # 订货类型 0-产品订货+资料订货 1-产品订货 2-资料订货 3-定制品订货 4-赠品领取 5-配件订货
    "orderWay": 0,  # 下单方式 0-空, 1-自购,2-代购,99-全选
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "productStatus": 0,  # 产品状态 0- 已上架或已下架 6-待生效 7-已上架 8-已下架 9-待生效或已上架
    "productTitle": "",  # 商品名称
    "productType": 0,  # 产品类型 ，1-普通商品，2-定制商品，3-组合商品
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_disInventory_getDisInventoryProductList(data=data, headers=headers):
    """
    获取分级押货有库存商品列表
    /mgmt/product/disInventory/getDisInventoryProductList

    参数说明:
    - catalogId: 商品分类Id
    - exact: 搜索是否模糊(0模糊,1精确)
    - exactSerialNos: 精确商品编码
    - isActivateItem: 是否升级商品 1-是 0-否
    - isConsumeStock: 是否仅消耗服务中心库存 0-否 1-是
    - isExchangeProduct: 是否换购商品 0-否 1-是
    - isFilterCusProduct: 是否过滤掉定制产品 0-否 1-是，默认为0
    - isPreProduct: 是否预售产品 1-是，0-否
    - isSignProduct: 是否签约购产品 1-是，0-否
    - isStopSale: 是否停止销售呈报 0-否 1-是
    - orderType: 订货类型 0-产品订货+资料订货 1-产品订货 2-资料订货 3-定制品订货 4-赠品领取 5-配件订货
    - orderWay: 下单方式 0-空, 1-自购,2-代购,99-全选
    - productStatus: 产品状态 0- 已上架或已下架 6-待生效 7-已上架 8-已下架 9-待生效或已上架
    - productTitle: 商品名称
    - productType: 产品类型 ，1-普通商品，2-定制商品，3-组合商品
    - serialNo: 商品编码
    """

    url = "/mgmt/product/disInventory/getDisInventoryProductList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
