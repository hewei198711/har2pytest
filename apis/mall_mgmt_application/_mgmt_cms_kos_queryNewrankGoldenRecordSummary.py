import os

from util.client import client

data = {
    "activityName": "",  # 活动名称
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # 分公司编号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "status": 0,  # 状态值
    "syncTimeEnd": "",  # 同步时间查询结束时间
    "syncTimeStart": "",  # 同步时间查询开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_queryNewrankGoldenRecordSummary(data=data, headers=headers):
    """
    查询KOS矩阵通金豆奖励记录汇总
    /mgmt/cms/kos/queryNewrankGoldenRecordSummary

    参数说明:
    - activityName: 活动名称
    - cardNo: 会员卡号
    - companyCode: 分公司编号
    - pageNum: 页码
    - pageSize: 每页页数
    - status: 状态值
    - syncTimeEnd: 同步时间查询结束时间
    - syncTimeStart: 同步时间查询开始时间
    """

    url = "/mgmt/cms/kos/queryNewrankGoldenRecordSummary"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
