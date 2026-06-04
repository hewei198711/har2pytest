import os

from util.client import client

params = {
    "asc": False,  # 是否升序:true-升序,false-降序
    "couponName": "",  # 优惠券名称
    "couponNumber": "",  # 优惠券编号
    "createTimeEnd": "",  # 创建时间止区
    "createTimeStart": "",  # 创建时间起区
    "offShelvesTime": "",  # 下架时间起区
    "offShelvesTimeEnd": "",  # 下架时间止期
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "platforms": [],  # 上架平台:1-APP,2-PC,4-小程序
    "shelvesChannels": [],  # 上架入口:1-商品详情,2-领券中心
    "shelvesTime": "",  # 上架时间起区
    "shelvesTimeEnd": "",  # 上架时间止期
    "sortBy": 0,  # 排序字段:1-创建时间,2-最后编辑时间,3-展示顺序
    "state": 0,  # 状态:1-待审核,2-待上架,3-已上架,4-已驳回,5-草稿,6-已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_state_shelvesCoupon(params=params, headers=headers):
    """
    领券中心各状态数量
    /mgmt/prmt/state/shelvesCoupon

    参数说明:
    - asc: 是否升序:true-升序,false-降序
    - couponName: 优惠券名称
    - couponNumber: 优惠券编号
    - createTimeEnd: 创建时间止区
    - createTimeStart: 创建时间起区
    - offShelvesTime: 下架时间起区
    - offShelvesTimeEnd: 下架时间止期
    - pageNum: 当前页
    - pageSize: 每页数量
    - platforms: 上架平台:1-APP,2-PC,4-小程序
    - shelvesChannels: 上架入口:1-商品详情,2-领券中心
    - shelvesTime: 上架时间起区
    - shelvesTimeEnd: 上架时间止期
    - sortBy: 排序字段:1-创建时间,2-最后编辑时间,3-展示顺序
    - state: 状态:1-待审核,2-待上架,3-已上架,4-已驳回,5-草稿,6-已下架
    """

    url = "/mgmt/prmt/state/shelvesCoupon"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
