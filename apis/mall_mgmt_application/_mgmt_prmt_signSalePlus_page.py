import os

from util.client import client

params = {
    "createTimeMax": "",  # 创建时间末
    "createTimeMin": "",  # 创建时间始
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "periodTimeMax": "",  # 活动有效期末
    "periodTimeMin": "",  # 活动有效期始
    "promotionCode": "",  # 活动编码
    "promotionName": "",  # 活动名称
    "promotionNameOrCode": "",  # 活动名称或编码
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "promotionStates": [],  # 活动状态集合:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "serialNo": "",  # 活动产品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSalePlus_page(params=params, headers=headers):
    """
    分页查询活动
    /mgmt/prmt/signSalePlus/page

    参数说明:
    - createTimeMax: 创建时间末
    - createTimeMin: 创建时间始
    - pageNum: 当前页
    - pageSize: 每页数量
    - periodTimeMax: 活动有效期末
    - periodTimeMin: 活动有效期始
    - promotionCode: 活动编码
    - promotionName: 活动名称
    - promotionNameOrCode: 活动名称或编码
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - promotionStates: 活动状态集合:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - serialNo: 活动产品编码
    """

    url = "/mgmt/prmt/signSalePlus/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
