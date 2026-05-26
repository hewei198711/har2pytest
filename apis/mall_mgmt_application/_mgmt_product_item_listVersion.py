import os

from util.client import client

data = {
    "versionStatus": "",  # 状态：1-草稿，2-待产品审核，3-产品审核不通过，4-待财务审核，5-财务审核不通过，6-待生效，7-已上架，8-已下架
    "pageNum": 1,  # 页码
    "pageSize": 10,  # 页面大小
    "serialNo": None,  # 商品编码
    "title": None,  # 商品名称
    "catalogId": None,  # 类型id
    "saleCompanyId": None,  # 销售主体id
    "orderType": 4,  # 订单类型，1-产品订货，2-资料订货，3-订制品订货
    "directSale": None,  # 是否直销，1-是，0-否
    "orderWay": None,  # 下单方式 1-自购,2-代购
    "deliverWay": None,  # 交付方式 1-公司交付,2-门店交付
    "tagTitle": None,  # 产品标签
    "slogan": None,  # 宣传标语
    "trademarkTitle": None,  # 商标产品名称
    "startTime": "",  # 开始时间时间戳
    "endTime": "",  # 结束时间时间戳
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
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
