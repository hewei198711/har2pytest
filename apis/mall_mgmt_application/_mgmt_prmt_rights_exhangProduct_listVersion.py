import os

from util.client import client

data = {
    "exchangeNo": "",  # 兑换产品编码
    "keyword": "",  # 搜索条件
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "set": 0,  # 顺序:0倒序;1正序
    "title": "",  # 兑换产品名称
    "updateEndTime": "",  # 更新时间结束(yyyy-MM-dd)
    "updateStartTime": "",  # 更新时间开始(yyyy-MM-dd)
    "versionStatus": 0,  # 状态：1-草稿，2-待审核，3-审核不通过，4-待生效，5-已上架，6-已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_exhangProduct_listVersion(data=data, headers=headers):
    """
    兑换产品版本列表
    /mgmt/prmt/rights/exhangProduct/listVersion

    参数说明:
    - exchangeNo: 兑换产品编码
    - keyword: 搜索条件
    - pageNum: 当前页
    - pageSize: 每页数量
    - set: 顺序:0倒序;1正序
    - title: 兑换产品名称
    - updateEndTime: 更新时间结束(yyyy-MM-dd)
    - updateStartTime: 更新时间开始(yyyy-MM-dd)
    - versionStatus: 状态：1-草稿，2-待审核，3-审核不通过，4-待生效，5-已上架，6-已下架
    """

    url = "/mgmt/prmt/rights/exhangProduct/listVersion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
