import os

from util.client import client

data = {
    "courseId": 0,  # 学堂课程id
    "keyword": "",  # 查询关键词
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_edu_queryEduCourses(data=data, headers=headers):
    """
    edu-获取油葱学堂课程分页
    /mgmt/edu/queryEduCourses

    参数说明:
    - courseId: 学堂课程id
    - keyword: 查询关键词
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/edu/queryEduCourses"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
