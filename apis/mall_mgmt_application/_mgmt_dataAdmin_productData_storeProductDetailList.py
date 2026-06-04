import os

from util.client import client

params = {
    "dateType": 0,  # 时间类型 0:天; 1:月; 2:年
    "endTime": "",  # 结束时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "productCode": "",  # 产品编码
    "set": 0,  # 顺序:0倒序;1正序
    "sortType": 0,  # 排序类型：0销售数量；1退货数量
    "startTime": "",  # 开始时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_productData_storeProductDetailList(params=params, headers=headers):
    """
    查询门店产品明细
    /mgmt/dataAdmin/productData/storeProductDetailList

    参数说明:
    - dateType: 时间类型 0:天; 1:月; 2:年
    - endTime: 结束时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - productCode: 产品编码
    - set: 顺序:0倒序;1正序
    - sortType: 排序类型：0销售数量；1退货数量
    - startTime: 开始时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - storeCode: 店铺编号
    """

    url = "/mgmt/dataAdmin/productData/storeProductDetailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
