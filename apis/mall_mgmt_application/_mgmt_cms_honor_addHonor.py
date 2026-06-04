import os

from util.client import client

data = {
    "cardNo": "",  # 用户卡号
    "userHonors": [{"honor": 0}],  # 荣誉称号列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_addHonor(data=data, headers=headers):
    """
    新增用户荣誉
    /mgmt/cms/honor/addHonor

    参数说明:
    - cardNo: 用户卡号
    - userHonors: 荣誉称号列表
    - userHonors.honor: 荣誉称号: 1.业务发展委员 2.健康食品委员 3.美容养肤委员 4.居家生活委员 5.系统教育委员 6.轻创业工作小组 7.全球卓越委员 8.分公司业务发展委员 9.公共营养师 10.健康管理顾问 11.展业先锋店 12.健康中国·推广大使
    """

    url = "/mgmt/cms/honor/addHonor"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
