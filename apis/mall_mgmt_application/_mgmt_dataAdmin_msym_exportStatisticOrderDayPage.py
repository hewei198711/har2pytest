import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "endCreateTime": "",  # 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "startCreateTime": "",  # 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_msym_exportStatisticOrderDayPage(params=params, headers=headers):
    """
    导出码上有名每日订单数据
    /mgmt/dataAdmin/msym/exportStatisticOrderDayPage

    参数说明:
    - cardNo: 会员卡号
    - endCreateTime: 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - startCreateTime: 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - storeCode: 服务中心编号
    """

    url = "/mgmt/dataAdmin/msym/exportStatisticOrderDayPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
