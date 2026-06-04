import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "enabled": False,  # 是否已启用:true-已启用,false-已禁用
    "id": 0,  # 活动主键
    "importKey": "",  # 导入操作键
    "keyword": "",  # 查询关键字:会员卡号或注册手机号
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


def _mgmt_prmt_complex_exportLimit(params=params, headers=headers):
    """
    导出可购顾客
    /mgmt/prmt/complex/exportLimit

    参数说明:
    - cardNo: 会员卡号
    - enabled: 是否已启用:true-已启用,false-已禁用
    - id: 活动主键
    - importKey: 导入操作键
    - keyword: 查询关键字:会员卡号或注册手机号
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - realName: 会员姓名
    - sourceChannel: 操作入口:1-新增或编辑页面,2-详情页面
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/complex/exportLimit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
