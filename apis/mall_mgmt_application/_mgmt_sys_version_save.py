import os

from util.client import client

data = {
    "apkUrl": "",  # 升级下载地址
    "auditStatus": 0,  # 审核状态: 1-审核中 2-审核通过
    "cardNo": "",  # 提审会员卡号
    "clientUseragent": "",  # 渠道的，每个用分号隔开，默认all
    "clientVersion": "",  # 版本号
    "id": 0,  # 主键id
    "memberTypeList": [],  # 顾客身份集合:1-会员 2-Vip会员 3-云商 4-微店
    "platformType": 0,  # app平台：1->android,2->ios,3-鸿蒙
    "thirdLoginStatus": 0,  # 第三方登录显示状态：1->显示，0->不显示
    "updateInstall": 0,  # 是否强制更新:1-是;0-否;2-不做任何处理
    "updateLog": "",  # 升级日志
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_version_save(data=data, headers=headers):
    """
    新增版本信息
    /mgmt/sys/version/save

    参数说明:
    - apkUrl: 升级下载地址
    - auditStatus: 审核状态: 1-审核中 2-审核通过
    - cardNo: 提审会员卡号
    - clientUseragent: 渠道的，每个用分号隔开，默认all
    - clientVersion: 版本号
    - id: 主键id
    - memberTypeList: 顾客身份集合:1-会员 2-Vip会员 3-云商 4-微店
    - platformType: app平台：1->android,2->ios,3-鸿蒙
    - thirdLoginStatus: 第三方登录显示状态：1->显示，0->不显示
    - updateInstall: 是否强制更新:1-是;0-否;2-不做任何处理
    - updateLog: 升级日志
    """

    url = "/mgmt/sys/version/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
