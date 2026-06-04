import os

from util.client import client

params = {
    "asc": False,  # 是否升序:true-升序,false-降序
    "id": 0,  # 登录提醒id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "sortBy": 0,  # 排序字段:1-分享次数,2-访问次数,3-访问人数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_exportShareStatistics(params=params, headers=headers):
    """
    导出分享统计
    /mgmt/prmt/loginGift/exportShareStatistics

    参数说明:
    - asc: 是否升序:true-升序,false-降序
    - id: 登录提醒id
    - pageNum: 当前页
    - pageSize: 每页数量
    - sortBy: 排序字段:1-分享次数,2-访问次数,3-访问人数
    """

    url = "/mgmt/prmt/loginGift/exportShareStatistics"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
