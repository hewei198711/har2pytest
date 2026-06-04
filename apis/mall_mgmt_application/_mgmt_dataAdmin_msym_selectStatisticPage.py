import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "selectTime": "",  # 查询数据时间 yyyy-MM-dd 注：当使用月份查询时,传该月01号
    "selectType": 0,  # 查询时间类型 1-日, 2-月
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_msym_selectStatisticPage(data=data, headers=headers):
    """
    码上有名-分页查询每日数据明细
    /mgmt/dataAdmin/msym/selectStatisticPage

    参数说明:
    - cardNo: 会员卡号
    - selectTime: 查询数据时间 yyyy-MM-dd 注：当使用月份查询时,传该月01号
    - selectType: 查询时间类型 1-日, 2-月
    - storeCode: 服务中心编号
    """

    url = "/mgmt/dataAdmin/msym/selectStatisticPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
