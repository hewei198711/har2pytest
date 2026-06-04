import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "finishTimeMax": "",  # 完成时间止yyyy-MM-dd
    "finishTimeMin": "",  # 完成时间起yyyy-MM-dd
    "getPlatform": 0,  # 领取平台1APP2PC4小程序
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "realName": "",  # 真实姓名
    "shareState": 0,  # 任务状态1进行中2未拼成3已拼成4已过期5已抢完
    "shareTaskId": 0,  # 分享活动id
    "shareTimeMax": "",  # 发起时间止yyyy-MM-dd
    "shareTimeMin": "",  # 发起时间起yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectTaskRecordPage(params=params, headers=headers):
    """
    分页查询分享记录
    /mgmt/prmt/share/selectTaskRecordPage

    参数说明:
    - cardNo: 会员卡号
    - finishTimeMax: 完成时间止yyyy-MM-dd
    - finishTimeMin: 完成时间起yyyy-MM-dd
    - getPlatform: 领取平台1APP2PC4小程序
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页条数
    - realName: 真实姓名
    - shareState: 任务状态1进行中2未拼成3已拼成4已过期5已抢完
    - shareTaskId: 分享活动id
    - shareTimeMax: 发起时间止yyyy-MM-dd
    - shareTimeMin: 发起时间起yyyy-MM-dd
    """

    url = "/mgmt/prmt/share/selectTaskRecordPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
