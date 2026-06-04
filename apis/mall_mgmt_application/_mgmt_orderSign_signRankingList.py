import os

from util.client import client

data = {
    "companyCode": "",  # 业务分公司编号
    "companyCodes": [],  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "set": 0,  # 顺序:0倒序;1正序
    "signEndTime": "",  # 签约结束月份
    "signStartTime": "",  # 签约开始月份
    "sortType": 0,  # 排序类型 0=签约（人）次数 , 1= 签约（人）次数-全国排名 ,2=已交付套装总量 , 3=已交付套装总量-全国排名
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_signRankingList(data=data, headers=headers):
    """
    运营后台-时光荟签约购排名榜
    /mgmt/orderSign/signRankingList

    参数说明:
    - companyCode: 业务分公司编号
    - set: 顺序:0倒序;1正序
    - signEndTime: 签约结束月份
    - signStartTime: 签约开始月份
    - sortType: 排序类型 0=签约（人）次数 , 1= 签约（人）次数-全国排名 ,2=已交付套装总量 , 3=已交付套装总量-全国排名
    - storeCode: 服务中心编号
    """

    url = "/mgmt/orderSign/signRankingList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
