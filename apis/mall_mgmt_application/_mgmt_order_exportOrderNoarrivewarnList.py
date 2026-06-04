import os

from util.client import client

data = {
    "arrivedFlag": False,  # 货到代收点标识，false：否；true：已签收
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客会员卡
    "followEndTime": "",  # 跟进结束时间
    "followStartTime": "",  # 跟进开始时间
    "followStatus": 0,  # 跟进状态 1->待跟进 2->已跟进 3->跟进中
    "from": 0,  # TODO: 添加参数说明
    "handleEndTime": "",  # 处理结束时间
    "handleStartTime": "",  # 处理开始时间
    "orderNo": "",  # 订单编号
    "orderType": "",  # 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 9->签约购转分订单 10->配件订单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exportOrderNoarrivewarnList(data=data, headers=headers):
    """
    导出订单货物未送达预警列表
    /mgmt/order/exportOrderNoarrivewarnList

    参数说明:
    - arrivedFlag: 货到代收点标识，false：否；true：已签收
    - creatorCard: 开单人卡号
    - customerCard: 顾客会员卡
    - followEndTime: 跟进结束时间
    - followStartTime: 跟进开始时间
    - followStatus: 跟进状态 1->待跟进 2->已跟进 3->跟进中
    - handleEndTime: 处理结束时间
    - handleStartTime: 处理开始时间
    - orderNo: 订单编号
    - orderType: 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 9->签约购转分订单 10->配件订单
    - pageNum: 页数
    - pageSize: 每页显示数
    - storeCode: 服务中心编号
    """

    url = "/mgmt/order/exportOrderNoarrivewarnList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
