import os

from util.client import client

params = {
    "businessMode": 0,  # 保证金类型，1/1:3，2/85%
    "from": 0,  # TODO: 添加参数说明
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "performanceTargetEnd": 0,  # 业绩目标结束
    "performanceTargetStart": 0,  # 业绩目标起始
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "year": 0,  # 业绩年份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getPerformanceAppraisalList(params=params, headers=headers):
    """
    查询服务中心业绩目标列表
    /mgmt/store/getPerformanceAppraisalList

    参数说明:
    - businessMode: 保证金类型，1/1:3，2/85%
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - pageNum: 页数
    - pageSize: 每页显示数
    - performanceTargetEnd: 业绩目标结束
    - performanceTargetStart: 业绩目标起始
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - year: 业绩年份
    """

    url = "/mgmt/store/getPerformanceAppraisalList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
