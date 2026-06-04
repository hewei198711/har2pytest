import os

from util.client import client

data = {
    "auditOpinion": "",  # 审核意见
    "auditResult": 0,  # 审核结果：1->审核通过；2->审核不通过
    "files": [{"receiverName": "", "receiverUrl": ""}],  # 附件
    "id": 0,  # 公告ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_mgmt_msg_notice_doNoticeAudit(data=data, headers=headers):
    """
    执行公告审核
    /mgmt/msgadmin/mgmt/msg/notice/doNoticeAudit

    参数说明:
    - auditOpinion: 审核意见
    - auditResult: 审核结果：1->审核通过；2->审核不通过
    - files: 附件
    - files.receiverName: 文件名
    - files.receiverUrl: url地址
    - id: 公告ID
    """

    url = "/mgmt/msgadmin/mgmt/msg/notice/doNoticeAudit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
