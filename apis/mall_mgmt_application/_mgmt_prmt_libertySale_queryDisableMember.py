import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "enabled": False,  # 是否已启用:true-已启用,false-已禁用
    "id": 0,  # 活动主键
    "importKey": "",  # 导入操作键
    "memberId": 0,  # TODO: 添加参数说明
    "memberType": 0,  # TODO: 添加参数说明
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "realName": "",  # 会员姓名
    "sourceChannel": 0,  # 操作入口:1-新增或编辑页面,2-详情页面
    "type": 0,  # 领券中心导入顾客类型：0-上架对象，1-领取对象
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_libertySale_queryDisableMember(data=data, headers=headers):
    """
    详情与编辑页/活动详情页 查询不可购会员信息
    /mgmt/prmt/libertySale/queryDisableMember

    参数说明:
    - cardNo: 会员卡号
    - enabled: 是否已启用:true-已启用,false-已禁用
    - id: 活动主键
    - importKey: 导入操作键
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - realName: 会员姓名
    - sourceChannel: 操作入口:1-新增或编辑页面,2-详情页面
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/libertySale/queryDisableMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
