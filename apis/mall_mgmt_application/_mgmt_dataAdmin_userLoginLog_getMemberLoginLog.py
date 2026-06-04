import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "loginDate": "",  # 登录时间 格式yyyy-MM-dd HH:mm:ss 时间段用逗号分隔
    "pageNum": 0,  # 页码(不传默认为1)
    "pageSize": 0,  # 每页大小(不传默认为10)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userLoginLog_getMemberLoginLog(params=params, headers=headers):
    """
    用户登录日志查询
    /mgmt/dataAdmin/userLoginLog/getMemberLoginLog

    参数说明:
    - cardNo: 会员卡号
    - loginDate: 登录时间 格式yyyy-MM-dd HH:mm:ss 时间段用逗号分隔
    - pageNum: 页码(不传默认为1)
    - pageSize: 每页大小(不传默认为10)
    """

    url = "/mgmt/dataAdmin/userLoginLog/getMemberLoginLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
