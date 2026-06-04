import os

from util.client import client

data = {
    "createTimeEnd": "",  # 创建时间查询：结束时间
    "createTimeStart": "",  # 创建时间查询：开始时间
    "isRecycle": 0,  # 是否查询回收站 1.是 0.否
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 显示条数
    "questionnaireStatus": 0,  # 问卷状态 -3:待生效;-2:草稿;-1:未发布;0:收集中;1:已结束;2：待审核;3:审核不通过
    "questionnaireTitle": "",  # 问卷标题
    "timeSort": "",  # 创建时间排序 desc：倒序  asc：正序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_queryQuestionnaire(data=data, headers=headers):
    """
    查询问卷列表
    /mgmt/cms/questionnaire/queryQuestionnaire

    参数说明:
    - createTimeEnd: 创建时间查询：结束时间
    - createTimeStart: 创建时间查询：开始时间
    - isRecycle: 是否查询回收站 1.是 0.否
    - pageNum: 页码
    - pageSize: 显示条数
    - questionnaireStatus: 问卷状态 -3:待生效;-2:草稿;-1:未发布;0:收集中;1:已结束;2：待审核;3:审核不通过
    - questionnaireTitle: 问卷标题
    - timeSort: 创建时间排序 desc：倒序  asc：正序
    """

    url = "/mgmt/cms/questionnaire/queryQuestionnaire"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
