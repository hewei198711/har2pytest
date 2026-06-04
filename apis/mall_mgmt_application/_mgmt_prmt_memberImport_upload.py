import os

from util.client import client

data = {
    "fileList": [{"fileName": "", "fileUrl": ""}],  # 文件列表
    "id": 0,  # 活动主键
    "immediately": False,  # 是否直接开始导入
    "importKey": "",  # 导入操作键
    "promotionParam": {"independentLimit": 0, "limitType": 0, "serialNos": []},  # 活动参数，限购方式为按需导入需传入
    "sourceChannel": 0,  # 操作入口，签约购活动参数:1-新增或编辑页面,2-详情页面
    "sourceType": 0,  # 来源类型:1-活动,2-优惠券派发,3-登录提醒,4-领券中心(上架对象),5-分享领券（分享人）,6-分享领券（助力人）,7-抽奖活动(活动顾客),8-抽奖活动(不可参加顾客),9-优惠券派发（不派发顾客）,10-签约购活动,11-签约购活动（不可购顾客）,12-签约购活动历史表,13-签约购活动（可购顾客）,14-随心购活动,15-随心购活动（可购顾客）,16-随心购活动（不可购顾客）,17-C端转赠优惠券对象限制,18-签约购活动3.0,19-签约购活动3.0(不可购顾客),20-签约购活动3.0历史表,21-签约购活动3.0(可购顾客)22-领券中心(领取对象),23-3S组合活动,24-3S组合活动(可购顾客),25-3S组合活动(不可购顾客)26-签约购4.0活动,27-签约购4.0活动(不可购顾客),28-签约购4.0活动历史表,29-签约购4.0活动(可购顾客)
    "type": 0,  # 领券中心导入顾客类型：0-上架对象，1-领取对象
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_memberImport_upload(data=data, headers=headers):
    """
    上传文件
    /mgmt/prmt/memberImport/upload

    参数说明:
    - fileList: 文件列表
    - fileList.fileName: 文件名称
    - fileList.fileUrl: 文件地址
    - id: 活动主键
    - immediately: 是否直接开始导入
    - importKey: 导入操作键
    - promotionParam: 活动参数，限购方式为按需导入需传入
    - promotionParam.independentLimit: 自定义独立限量1:开启;0:关闭
    - promotionParam.limitType: 限购方式:1不限量2独立限量3统一限量4按需导入5按阶梯配置(独立限量)6按阶梯配置(统一限量)
    - promotionParam.serialNos: 活动产品编码集合
    - sourceChannel: 操作入口，签约购活动参数:1-新增或编辑页面,2-详情页面
    - sourceType: 来源类型:1-活动,2-优惠券派发,3-登录提醒,4-领券中心(上架对象),5-分享领券（分享人）,6-分享领券（助力人）,7-抽奖活动(活动顾客),8-抽奖活动(不可参加顾客),9-优惠券派发（不派发顾客）,10-签约购活动,11-签约购活动（不可购顾客）,12-签约购活动历史表,13-签约购活动（可购顾客）,14-随心购活动,15-随心购活动（可购顾客）,16-随心购活动（不可购顾客）,17-C端转赠优惠券对象限制,18-签约购活动3.0,19-签约购活动3.0(不可购顾客),20-签约购活动3.0历史表,21-签约购活动3.0(可购顾客)22-领券中心(领取对象),23-3S组合活动,24-3S组合活动(可购顾客),25-3S组合活动(不可购顾客)26-签约购4.0活动,27-签约购4.0活动(不可购顾客),28-签约购4.0活动历史表,29-签约购4.0活动(可购顾客)
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/memberImport/upload"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
