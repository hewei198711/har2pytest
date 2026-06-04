import os

from util.client import client

data = {
    "catalogId": "",  # 类型id
    "deliverWay": 0,  # 交付方式 1-公司交付,2-门店交付
    "directSale": 0,  # 是否直销，1-是，0-否
    "endTime": 0,  # 结束时间时间戳
    "orderType": 0,  # 订单类型，1-产品订货，2-资料订货，3-订制品订货
    "orderWay": 0,  # 下单方式 1-自购,2-代购
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "saleCompanyId": "",  # 销售主体id
    "serialNo": "",  # 商品编码
    "slogan": "",  # 宣传标语
    "startTime": 0,  # 开始时间时间戳
    "tagTitle": "",  # 产品标签
    "title": "",  # 商品名称
    "trademarkTitle": "",  # 商标产品名称
    "versionStatus": "",  # 状态：1-草稿，2-待产品审核，3-产品审核不通过，4-待财务审核，5-财务审核不通过，6-待生效，7-已上架，8-已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_listVersion(data=data, headers=headers):
    """
    商品版本列表
    /mgmt/product/item/listVersion

    参数说明:
    - catalogId: 类型id
    - deliverWay: 交付方式 1-公司交付,2-门店交付
    - directSale: 是否直销，1-是，0-否
    - endTime: 结束时间时间戳
    - orderType: 订单类型，1-产品订货，2-资料订货，3-订制品订货
    - orderWay: 下单方式 1-自购,2-代购
    - pageNum: 页码
    - pageSize: 页面大小
    - saleCompanyId: 销售主体id
    - serialNo: 商品编码
    - slogan: 宣传标语
    - startTime: 开始时间时间戳
    - tagTitle: 产品标签
    - title: 商品名称
    - trademarkTitle: 商标产品名称
    - versionStatus: 状态：1-草稿，2-待产品审核，3-产品审核不通过，4-待财务审核，5-财务审核不通过，6-待生效，7-已上架，8-已下架
    """

    url = "/mgmt/product/item/listVersion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
