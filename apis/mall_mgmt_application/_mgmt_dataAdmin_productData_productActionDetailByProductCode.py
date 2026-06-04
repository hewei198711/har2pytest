import os

from util.client import client

params = {
    "dateType": 0,  # 时间类型 0:天 ; 1:月 ; 2: 年
    "endTime": "",  # 结束时间
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "productCode": "",  # 产品编码
    "set": 0,  # 顺序:0倒序;1正序
    "sortType": 0,  # 排序类型
    "source": "",  # 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    "sourceList": [],  # TODO: 添加参数说明
    "startTime": "",  # 开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_productData_productActionDetailByProductCode(params=params, headers=headers):
    """
    产品行为数据明细
    /mgmt/dataAdmin/productData/productActionDetailByProductCode

    参数说明:
    - dateType: 时间类型 0:天 ; 1:月 ; 2: 年
    - endTime: 结束时间
    - productCode: 产品编码
    - set: 顺序:0倒序;1正序
    - sortType: 排序类型
    - source: 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    - startTime: 开始时间
    """

    url = "/mgmt/dataAdmin/productData/productActionDetailByProductCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
