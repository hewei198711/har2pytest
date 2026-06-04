import os

from util.client import client

params = {
    "endMonth": 0,  # 结束月份
    "moneyType": 0,  # 本月余额类型, 1/余额为0 2/余额不为0
    "pageNum": 0,  # 页码，默认为1，为0查全部
    "pageSize": 0,  # 页面大小,默认为10,为0查全部
    "shopType": 0,  # 网点类型
    "startMonth": 0,  # 开始月份
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_countStoreDepositMonthList(params=params, headers=headers):
    """
    获取保证金月结统计
    /mgmt/store/countStoreDepositMonthList

    参数说明:
    - endMonth: 结束月份
    - moneyType: 本月余额类型, 1/余额为0 2/余额不为0
    - pageNum: 页码，默认为1，为0查全部
    - pageSize: 页面大小,默认为10,为0查全部
    - shopType: 网点类型
    - startMonth: 开始月份
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/store/countStoreDepositMonthList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
