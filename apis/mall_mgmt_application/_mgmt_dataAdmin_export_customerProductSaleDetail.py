import os

from util.client import client

data = {
    "customerCard": "",  # 会员卡号
    "dateType": 0,  # 时间类型 0:天 ; 1:月 ; 2: 年
    "endTime": "",  # 结束时间,yyyy-MM-dd
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "productCode": "",  # 产品编码
    "productName": "",  # 产品名称
    "set": 0,  # 顺序:0倒序;1正序
    "sortType": 0,  # 排序类型
    "startTime": "",  # 开始时间,yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_customerProductSaleDetail(data=data, headers=headers):
    """
    用户购买产品明细导出
    /mgmt/dataAdmin/export/customerProductSaleDetail

    参数说明:
    - customerCard: 会员卡号
    - dateType: 时间类型 0:天 ; 1:月 ; 2: 年
    - endTime: 结束时间,yyyy-MM-dd
    - productCode: 产品编码
    - productName: 产品名称
    - set: 顺序:0倒序;1正序
    - sortType: 排序类型
    - startTime: 开始时间,yyyy-MM-dd
    """

    url = "/mgmt/dataAdmin/export/customerProductSaleDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
