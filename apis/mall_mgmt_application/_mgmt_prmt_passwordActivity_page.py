import os

from util.client import client

params = {
    "createTimeMax": "",  # 创建时间末, 格式：yyyy-MM-dd 23:59:59
    "createTimeMin": "",  # 创建时间始, 格式：yyyy-MM-dd 00:00:00
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回(待修改),6-草稿,7-已失效,不传表示查询全部
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_passwordActivity_page(params=params, headers=headers):
    """
    分页查询口令活动列表
    /mgmt/prmt/passwordActivity/page

    参数说明:
    - createTimeMax: 创建时间末, 格式：yyyy-MM-dd 23:59:59
    - createTimeMin: 创建时间始, 格式：yyyy-MM-dd 00:00:00
    - pageNum: 当前页
    - pageSize: 每页数量
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回(待修改),6-草稿,7-已失效,不传表示查询全部
    """

    url = "/mgmt/prmt/passwordActivity/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
