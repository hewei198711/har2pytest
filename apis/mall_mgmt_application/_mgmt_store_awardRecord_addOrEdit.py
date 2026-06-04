import os

from util.client import client

data = {
    "awardDesc": "",  # 奖项说明
    "awardName": "",  # 奖项名称
    "awardPic": "",  # 获奖海报地址
    "businessType": 0,  # 经营模式  1是1:3, 是85折
    "effectTime": "",  # 生效时间  yyyy-MM-dd格式
    "expireTime": "",  # 失效时间  yyyy-MM-dd格式
    "fileName": "",  # 海报图片名称
    "isShowPc": 0,  # 是否展示于门店列表 0 是   1 否
    "leaderName": "",  # 负责人名称
    "leaderNo": "",  # 负责人卡号
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "wdTypeName": "",  # 网点类型名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_awardRecord_addOrEdit(data=data, headers=headers):
    """
    新增/编辑
    /mgmt/store/awardRecord/addOrEdit

    参数说明:
    - awardDesc: 奖项说明
    - awardName: 奖项名称
    - awardPic: 获奖海报地址
    - businessType: 经营模式  1是1:3, 是85折
    - effectTime: 生效时间  yyyy-MM-dd格式
    - expireTime: 失效时间  yyyy-MM-dd格式
    - fileName: 海报图片名称
    - isShowPc: 是否展示于门店列表 0 是   1 否
    - leaderName: 负责人名称
    - leaderNo: 负责人卡号
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - wdTypeName: 网点类型名称
    """

    url = "/mgmt/store/awardRecord/addOrEdit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
