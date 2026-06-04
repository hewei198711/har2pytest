import os

from util.client import client

data = {
    "dateType": 0,  # 时间类型 0:天 ; 1:月 ; 2: 年
    "endTime": "",  # 结束时间,yyyy-MM-dd
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "platform": 0,  # 平台  1->WEB商城 2->APP商城 3->小程序商城
    "productCode": "",  # 产品编号
    "set": 0,  # 顺序:0倒序;1正序
    "sortType": 0,  # 排序类型
    "startTime": "",  # 开始时间,yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_consumeList(data=data, headers=headers):
    """
    金豆兑换统计数据明细列表导出
    /mgmt/dataAdmin/export/consumeList

    参数说明:
    - dateType: 时间类型 0:天 ; 1:月 ; 2: 年
    - endTime: 结束时间,yyyy-MM-dd
    - platform: 平台  1->WEB商城 2->APP商城 3->小程序商城
    - productCode: 产品编号
    - set: 顺序:0倒序;1正序
    - sortType: 排序类型
    - startTime: 开始时间,yyyy-MM-dd
    """

    url = "/mgmt/dataAdmin/export/consumeList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
