import os

from util.client import client

data = {
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


def _mgmt_dataAdmin_msym_expressTypeList(data=data, headers=headers):
    """
    码上有名-配送方式统计(后台饼图)
    /mgmt/dataAdmin/msym/expressTypeList

    参数说明:
    - cardNo: 会员卡号
    - endCreateTime: 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - startCreateTime: 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - storeCode: 服务中心编号
    """

    url = "/mgmt/dataAdmin/msym/expressTypeList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
