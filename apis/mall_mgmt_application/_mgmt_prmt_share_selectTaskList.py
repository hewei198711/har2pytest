import os

from util.client import client

params = {
    "couponName": "",  # 优惠券名称
    "couponNumber": "",  # 优惠券编号
    "createTimeMax": "",  # 创建时间止
    "createTimeMin": "",  # 创建时间起
    "flag": False,  # 排序false降序 true升序
    "offShelfTimeMax": "",  # 下架时间止
    "offShelfTimeMin": "",  # 下架时间起
    "onShelfTimeMax": "",  # 上架时间止
    "onShelfTimeMin": "",  # 上架时间起
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "shelfPlatforms": [],  # 上架平台:1-APP,2-PC,4-小程序
    "sortColumn": 0,  # 排序字段1创建时间2更新时间3展示顺序
    "taskState": 0,  # 状态1待审核2待上架3已上架4已下架5已驳回6草稿
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectTaskList(params=params, headers=headers):
    """
    分享领券活动列表导出
    /mgmt/prmt/share/selectTaskList

    参数说明:
    - couponName: 优惠券名称
    - couponNumber: 优惠券编号
    - createTimeMax: 创建时间止
    - createTimeMin: 创建时间起
    - flag: 排序false降序 true升序
    - offShelfTimeMax: 下架时间止
    - offShelfTimeMin: 下架时间起
    - onShelfTimeMax: 上架时间止
    - onShelfTimeMin: 上架时间起
    - pageNum: 当前页
    - pageSize: 每页条数
    - shelfPlatforms: 上架平台:1-APP,2-PC,4-小程序
    - sortColumn: 排序字段1创建时间2更新时间3展示顺序
    - taskState: 状态1待审核2待上架3已上架4已下架5已驳回6草稿
    """

    url = "/mgmt/prmt/share/selectTaskList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
