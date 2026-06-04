import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "id": 0,  # TODO: 添加参数说明
    "importKey": "",  # 导入操作键
    "independentLimit": 0,  # 自定义独立限量1:开启;0:关闭
    "limitNumber": 0,  # 限购数量(-1不限,-2按需分配)
    "limitTotalCount": 0,  # 购买数量上限（自定义独立限量为开启时必填）
    "limitType": 0,  # 限购方式1不限量2独立限量3统一限量4按需导入5按PV阶梯配置6按阶梯统一限制
    "mobile": "",  # 注册手机号
    "productLists": [{"serialNo": "", "totalCount": 0}],  # 商品和数量集合
    "promotionId": 0,  # 活动id
    "realName": "",  # 会员姓名
    "serialNo": "",  # 商品编码
    "totalCount": 0,  # 可购买数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_addUser(data=data, headers=headers):
    """
    手动新增活动用户
    /mgmt/prmt/addUser

    参数说明:
    - cardNo: 会员卡号
    - importKey: 导入操作键
    - independentLimit: 自定义独立限量1:开启;0:关闭
    - limitNumber: 限购数量(-1不限,-2按需分配)
    - limitTotalCount: 购买数量上限（自定义独立限量为开启时必填）
    - limitType: 限购方式1不限量2独立限量3统一限量4按需导入5按PV阶梯配置6按阶梯统一限制
    - mobile: 注册手机号
    - productLists: 商品和数量集合
    - productLists.serialNo: 商品编码
    - productLists.totalCount: 可购买数量
    - promotionId: 活动id
    - realName: 会员姓名
    - serialNo: 商品编码
    - totalCount: 可购买数量
    """

    url = "/mgmt/prmt/addUser"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
