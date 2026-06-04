import os

from util.client import client

data = {
    "awardDesc": "",  # 获奖说明
    "awardName": "",  # 奖项名称
    "endCreateTime": "",  # 提交时间(结束) yyyy-MM-dd
    "endEffectTime": "",  # 生效时间(结束) yyyy-MM-dd
    "endExpireTime": "",  # 失效时间(结束) yyyy-MM-dd
    "flag": 0,  # 是否展示已失效,生效中记录  0 是,其他则否
    "id": 0,  # 主键id
    "isShowPc": 0,  # 是否展示于门店列表 0 是   1 否
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "startCreateTime": "",  # 提交时间(开始) yyyy-MM-dd
    "startEffectTime": "",  # 生效时间(开始) yyyy-MM-dd
    "startExpireTime": "",  # 失效时间(开始) yyyy-MM-d
    "status": 0,  # 弹窗状态 0 待生效，1 生效中， 2 已失效
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "wdTypeName": "",  # 网点类型名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_awardRecord_pageList(data=data, headers=headers):
    """
    分页列表
    /mgmt/store/awardRecord/pageList

    参数说明:
    - awardDesc: 获奖说明
    - awardName: 奖项名称
    - endCreateTime: 提交时间(结束) yyyy-MM-dd
    - endEffectTime: 生效时间(结束) yyyy-MM-dd
    - endExpireTime: 失效时间(结束) yyyy-MM-dd
    - flag: 是否展示已失效,生效中记录  0 是,其他则否
    - id: 主键id
    - isShowPc: 是否展示于门店列表 0 是   1 否
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - pageNum: 页码
    - pageSize: 每页页数
    - startCreateTime: 提交时间(开始) yyyy-MM-dd
    - startEffectTime: 生效时间(开始) yyyy-MM-dd
    - startExpireTime: 失效时间(开始) yyyy-MM-d
    - status: 弹窗状态 0 待生效，1 生效中， 2 已失效
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - wdTypeName: 网点类型名称
    """

    url = "/mgmt/store/awardRecord/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
