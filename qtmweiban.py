import json
import time

import requests

listCategory_url = 'https://weiban.mycourse.cn/pharos/usercourse/listCategory.do'
listCourse_url = 'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do'
finishCourse_url = 'https://weiban.mycourse.cn/pharos/usercourse/finish.do'

count = 0

# 学校代码和令牌码以及userId、userProjectId通过网页登陆后获取
# 仅需填写下方四个值即可实现自动化刷课
tenantCode = ''       # 学校代码
token = ''            # 令牌
userId = ''
userProjectId = ''

categoryCode = ''
userCourseId = ''
chooseType = '3'


listCategory_PostBody = {'chooseType': chooseType, 'tenantCode': tenantCode,
                         'token': token, 'userId': userId, 'userProjectId': userProjectId}
listCourse_PostBody = {'categoryCode': categoryCode, 'chooseType': chooseType,
                       'tenantCode': tenantCode, 'token': token, 'userId': userId, 'userProjectId': userProjectId}
finishCourse_params = {

    'userCourseId': userCourseId,
    'tenantCode': tenantCode
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

res1 = requests.post(listCategory_url, headers=headers,
                     data=listCategory_PostBody)
res1.encoding = 'utf-8'
# res1.json
# print(json.loads(res1.text)['data'])
# print(res1.text["data"])

for category in json.loads(res1.text)['data']:
    # print(category['categoryCode'] + ' ' + category['categoryName'])
    listCourse_PostBody['categoryCode'] = category['categoryCode']
    res2 = requests.post(listCourse_url, headers=headers,
                         data=listCourse_PostBody)
    res2.encoding = 'utf-8'
    res2text = json.loads(res2.text)
    # print(res2text)
    for data in res2text['data']:
        userCourseId = data['userCourseId']
        if data['finished'] == 2:

            # 请求study.do
            r1 = requests.post(
                'https://weiban.mycourse.cn/pharos/usercourse/study.do',
                headers=headers,
                data={'courseId': data['resourceId'],
                      'tenantCode': tenantCode,
                      'token': token,
                      'userId': userId,
                      'userProjectId': userProjectId},
                params={'timestamp': int(time.time())})
            # r1.encoding='utf-8'
            # print(data['resourceId'])
            # print(data['resourceName'])
            # print(r1.text)
            # exit()
            time.sleep(10)

            # finishCourse
            finishCourse_params['userCourseId'] = data['userCourseId']
            finishCourse_params['timestamp'] = int(time.time())
            res3 = requests.get(
                finishCourse_url, headers=headers, params=finishCourse_params)
            # res3.encoding = 'utf-8'
            # print(json.loads(res3.text))
            count = count + 1
            print(str(count) + ' ' + data['resourceName'])

            time.sleep(0.5)
            # break
        else:
            continue

        # print(userCourseId)
    # break
