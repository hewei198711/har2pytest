import os

from util.client import client

data = {
    "contractType": 0,  # 合同类型，1/经营合同（默认），2/协议
    "leaderId": 0,  # 负责人id
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "managerName": "",  # 经营者姓名
    "memberId": 0,  # 会员id
    "remark": "",  # 备注
    "signType": 0,  # 签署类型：1/单方签署，2/双方签署，3/三方签署
    "spouseName": "",  # 配偶姓名
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "templateNo": "",  # 合同模板编号
    "year": "",  # 年度
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_addAndSubmitContract(data=data, headers=headers):
    """
    保存并提交合同
    /mgmt/store/addAndSubmitContract

    参数说明:
    - contractType: 合同类型，1/经营合同（默认），2/协议
    - leaderId: 负责人id
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - managerName: 经营者姓名
    - memberId: 会员id
    - remark: 备注
    - signType: 签署类型：1/单方签署，2/双方签署，3/三方签署
    - spouseName: 配偶姓名
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - templateNo: 合同模板编号
    - year: 年度
    """

    url = "/mgmt/store/addAndSubmitContract"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
