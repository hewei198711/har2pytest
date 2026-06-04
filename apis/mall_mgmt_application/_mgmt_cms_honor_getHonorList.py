import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "mobile": "",  # 注册手机号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "userHonors": [{"honor": 0}],  # 荣誉称号列表
    "userName": "",  # 姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_getHonorList(data=data, headers=headers):
    """
    获取用户荣誉称号列表
    /mgmt/cms/honor/getHonorList

    参数说明:
    - cardNo: 会员卡号
    - mobile: 注册手机号
    - pageNum: 页码
    - pageSize: 每页页数
    - userHonors: 荣誉称号列表
    - userHonors.honor: 荣誉称号: 1.业务发展委员 2.健康食品委员 3.美容养肤委员 4.居家生活委员 5.系统教育委员 6.轻创业工作小组 7.全球卓越委员 8.分公司业务发展委员 9.公共营养师 10.健康管理顾问 11.展业先锋店 12.健康中国·推广大使
    - userName: 姓名
    """

    url = "/mgmt/cms/honor/getHonorList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
