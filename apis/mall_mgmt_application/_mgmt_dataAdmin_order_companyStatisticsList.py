import os

from util.client import client

params = {
    "endCreateTime": "",  # 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "endOrderMonth": "",  # 结束业绩月份yyyyMM 202104
    "orderRouteList": [],  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "serialNo": "",  # 产品编码
    "set": 0,  # 顺序:0倒序;1正序
    "sortType": 0,  # 排序类型
    "source": "",  # 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    "sourceList": [],  # TODO: 添加参数说明
    "startCreateTime": "",  # 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "startOrderMonth": "",  # 开始业绩月份yyyyMM 202104
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_order_companyStatisticsList(params=params, headers=headers):
    """
    查询业务分公司统计明细
    /mgmt/dataAdmin/order/companyStatisticsList

    参数说明:
    - endCreateTime: 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - endOrderMonth: 结束业绩月份yyyyMM 202104
    - serialNo: 产品编码
    - set: 顺序:0倒序;1正序
    - sortType: 排序类型
    - source: 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    - startCreateTime: 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - startOrderMonth: 开始业绩月份yyyyMM 202104
    """

    url = "/mgmt/dataAdmin/order/companyStatisticsList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
