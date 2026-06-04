import os

from util.client import client

params = {
    "assistCardNo": "",  # 分享人会员卡号
    "assistTimeMax": "",  # 助力时间止yyyy-MM-dd
    "assistTimeMin": "",  # 助力时间起yyyy-MM-dd
    "cardNo": "",  # 会员卡号
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


def _mgmt_prmt_share_selectAssistList(params=params, headers=headers):
    """
    查询助力记录导出
    /mgmt/prmt/share/selectAssistList

    参数说明:
    - assistCardNo: 分享人会员卡号
    - assistTimeMax: 助力时间止yyyy-MM-dd
    - assistTimeMin: 助力时间起yyyy-MM-dd
    - cardNo: 会员卡号
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页条数
    - realName: 真实姓名
    - shareState: 任务状态1进行中2未拼成3已拼成4已过期5已抢完
    - shareTaskId: 分享活动id
    - shareTimeMax: 发起时间止yyyy-MM-dd
    - shareTimeMin: 发起时间起yyyy-MM-dd
    """

    url = "/mgmt/prmt/share/selectAssistList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
