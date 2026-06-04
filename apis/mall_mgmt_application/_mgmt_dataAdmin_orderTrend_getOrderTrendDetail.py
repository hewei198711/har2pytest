import os

from util.client import client

params = {
    "achievementMonth": "",  # 业绩月份 格式yyyyMM 时间段用逗号分隔
    "contrastDate": "",  # 对比时间 格式yyyy-MM-dd 时间段用逗号分隔
    "orderDate": "",  # 订单时间 格式yyyy-MM-dd 时间段用逗号分隔
    "pageNum": 0,  # 页码(不传默认为1)
    "pageSize": 0,  # 每页大小(不传默认为10)
    "productCode": "",  # 产品编号
    "source": 0,  # 下单平台 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_orderTrend_getOrderTrendDetail(params=params, headers=headers):
    """
    获取订单数据走势-明细数据
    /mgmt/dataAdmin/orderTrend/getOrderTrendDetail

    参数说明:
    - achievementMonth: 业绩月份 格式yyyyMM 时间段用逗号分隔
    - contrastDate: 对比时间 格式yyyy-MM-dd 时间段用逗号分隔
    - orderDate: 订单时间 格式yyyy-MM-dd 时间段用逗号分隔
    - pageNum: 页码(不传默认为1)
    - pageSize: 每页大小(不传默认为10)
    - productCode: 产品编号
    - source: 下单平台 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    """

    url = "/mgmt/dataAdmin/orderTrend/getOrderTrendDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
