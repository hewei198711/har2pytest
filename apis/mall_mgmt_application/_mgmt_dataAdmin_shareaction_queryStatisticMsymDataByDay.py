import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "customerName": "",  # 顾客姓名
    "endDate": "",  # 结束日期,yyyy-MM-dd
    "memberType": 0,  # 顾客身份,2-VIP会员,3-云商,4-微店
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "startDate": "",  # 开始日期,格式yyyy-MM-dd
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_shareaction_queryStatisticMsymDataByDay(data=data, headers=headers):
    """
    查询码上有名数据明细列表
    /mgmt/dataAdmin/shareaction/queryStatisticMsymDataByDay

    参数说明:
    - cardNo: 会员卡号
    - customerName: 顾客姓名
    - endDate: 结束日期,yyyy-MM-dd
    - memberType: 顾客身份,2-VIP会员,3-云商,4-微店
    - startDate: 开始日期,格式yyyy-MM-dd
    - storeCode: 服务中心编号
    """

    url = "/mgmt/dataAdmin/shareaction/queryStatisticMsymDataByDay"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
