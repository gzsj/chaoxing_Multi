import requests
import time
import hashlib
import re
import os
import json
class GetAllInfo():
    def __init__(self,usernm,passwd):
        self.usernm = usernm
        self.passwd = passwd
        self.session = requests.session()
        self.user = {}
        self.course = {}
        self.jobs = {}
        self.ppt = {}
        self.mp4 = {}
    def login(self):
        header = {'Accept-Language': 'zh_CN',
                  'Content-Type': 'multipart/form-data; boundary=vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6',
                  'Host': 'passport2.chaoxing.com',
                  'Connection': 'Keep-Alive',
                  'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_1969814533'
                  }
        datas = ''
        datas += '--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6\r\nContent-Disposition: form-data; name="uname"\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n'
        datas += self.usernm + '\r\n'
        datas +='--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6\r\nContent-Disposition: form-data; name="code"\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n'
        datas += self.passwd + '\r\n'
        datas +='--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6\r\nContent-Disposition: form-data; name="loginType"\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n'
        datas +='1\r\n'
        datas += '--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6\r\nContent-Disposition: form-data; name="roleSelect"\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n'
        datas +='true\r\n--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6--\r\n'
        time_stamp = int(time.time() * 1000)
        m_token = '4faa8662c59590c6f43ae9fe5b002b42'
        m_encrypt_str = 'token=' + m_token + '&_time=' + str(time_stamp) + '&DESKey=Z(AfY@XS'
        md5 = hashlib.md5()
        md5.update(m_encrypt_str.encode('utf-8'))
        m_inf_enc = md5.hexdigest()
        post_url = 'http://passport2.chaoxing.com/xxt/loginregisternew?' + 'token=' + m_token + '&_time=' + str(time_stamp) + '&inf_enc=' + m_inf_enc
        req = self.session.post(post_url, data=datas, headers=header)
        result = req.json()
        if result['status']:
            print('{}登录成功'.format(self.usernm))
            if os.path.exists(os.path.join('saves',str(self.usernm))):
                pass
            else:
                os.mkdir(os.path.join('saves',str(self.usernm)))
            cookie = requests.utils.dict_from_cookiejar(self.session.cookies)
            self.user['fid'] = cookie['fid']
            self.user['userid'] = cookie['_uid']
            self.userinfo()
            self.find_courses()
            self.find_objectives()
            return self.usernm,self.user['name'],self.course['coursenm']
        else:
            print('{}登录有误，请检查您的账号密码'.format(self.usernm))



    def userinfo(self):
        url = 'http://i.mooc.chaoxing.com/settings/info'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        resq = self.session.get(url, headers=header)
        content = resq.text
        self.user['name'] = re.findall('<span id="resetRealnamespac" title="(.*?)">', content)[0]
        self.user['usernm'] = self.usernm
        self.user['passwd'] = self.passwd
    def find_courses(self):
        self.chapterids = []
        print("{}正在获取课程".format(self.usernm))
        header = {'Accept-Encoding': 'gzip',
                  'Accept-Language': 'zh_CN',
                  'Host': 'mooc1-api.chaoxing.com',
                  'Connection': 'Keep-Alive',
                  'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_1969814533'
                  }
        my_course = self.session.get("http://mooc1-api.chaoxing.com/mycourse?rss=1&mcode=", headers=header)
        result = my_course.json()
        channelList = result['channelList']
        for item in channelList:
            try:
                print(str(channelList.index(item)) + '、' + item['content']['course']['data'][0]['name'])
            except:
                print()
        num = int(input('请输入您要选择的课程的编号'))
        channelList_json = channelList[num]
        self.course['cpi'] = channelList_json['cpi']
        self.course['clazzid'] = channelList_json['content']['id']
        self.course['courseid'] = channelList_json['content']['course']['data'][0]['id']
        self.course['coursenm'] = channelList_json['content']['course']['data'][0]['name']
        print('{}要查看的课程为：'.format(self.usernm))
        print("课程名称:" + channelList[num]['content']['course']['data'][0]['name'])
        print("讲师：" + channelList[num]['content']['course']['data'][0]['teacherfactor'])
        url = 'https://mooc1-1.chaoxing.com/visit/stucoursemiddle?courseid=' + str(
            self.course['courseid']) + '&clazzid=' + str(self.course['clazzid']) + '&vc=1&cpi=' + str(self.course['cpi'])
        resq = self.session.get(url, headers=header)
        content = resq.content.decode('utf-8')
        for chapter in re.findall('\?chapterId=(.*?)&', content):
            self.chapterids.append(str(chapter))
        self.course['enc'] = re.findall("&clazzid=.*?&enc=(.*?)'", content)[0]

        url = 'https://mooc1-1.chaoxing.com/visit/stucoursemiddle?courseid={}&clazzid={}&vc=1&cpi={}'.format(
            self.course['courseid'], self.course['clazzid'], self.course['cpi'])
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        resq = self.session.get(url, headers=header)
        self.course['openc'] = re.findall("openc : '(.*?)'", resq.text)[0]

        path = os.path.join('saves',str(self.usernm),str(self.course['courseid']))
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        with open(os.path.join(path,'course.json'), 'w') as f:
            json.dump(self.course, f)
        with open(os.path.join(path,'user.json'), 'w') as f:
            json.dump(self.user, f)
        with open(os.path.join(path,'chapters.json'), 'w') as f:
            json.dump(self.chapterids,f)
        print('{}保存配置文件成功'.format(self.usernm))
    def find_objects(self,lesson_id,course_id):
        url = 'http://mooc1-api.chaoxing.com/gas/knowledge?id=' + str(lesson_id) + '&courseid=' + str(
            course_id) + '&fields=begintime,clickcount,createtime,description,indexorder,jobUnfinishedCount,jobcount,jobfinishcount,label,lastmodifytime,layer,listPosition,name,openlock,parentnodeid,status,id,card.fields(cardIndex,cardorder,description,knowledgeTitile,knowledgeid,theme,title,id).contentcard(all)&view=json'
        header = {
            'Accept-Language': 'zh_CN',
            'Host': 'mooc1-api.chaoxing.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_19698145335.21'
        }
        req = self.session.get(url, headers=header)
        content = str(json.loads(req.text)['data'][0]['card']['data']).replace('&quot;', '')
        result = re.findall('{objectid:(.*?),.*?,_jobid:(.*?),', content)
        self.jobs[lesson_id] = result
        print('{}在章节{}中找到{}个任务点'.format(self.usernm,lesson_id,len(result)))
    def find_objectives(self):
        for item in self.chapterids:
            self.find_objects(item, self.course['courseid'])
        with open(os.path.join('saves', str(self.usernm), str(self.course['courseid']), 'job_list.json'), 'w') as file:
            json.dump(self.jobs, file)
        print('{}完成添加{}任务点至json文件'.format(self.usernm,len(self.jobs)))
        try:
            with open(os.path.join('saves',str(self.usernm), str(self.course['courseid']), 'mp4_log.json'), 'r') as m:
                mm = json.loads(m.read())
            with open(os.path.join('saves',str(self.usernm), str(self.course['courseid']), 'ppt_log.json'), 'r') as p:
                pp = json.loads(p.read())
            if input('检测到已存在部分内容，是否继续(1/0)'):
                total = str(mm) + str(pp)
            else:
                total = ''
        except:
            total = ''
        for item in self.jobs:
            for i in self.jobs[item]:
                if i[0] in total:
                    print('{}已经存在'.format(i[0]))
                else:
                    self.determine_job_type(item,i,self.user['fid'])
        job_total = len(self.ppt) +len(self.mp4)
        with open(os.path.join('saves',str(self.usernm),str(self.course['courseid']),'mp4_log.json'),'w') as m_dump:
            json.dump(self.mp4,m_dump)
        with open(os.path.join('saves',str(self.usernm),str(self.course['courseid']),'ppt_log.json'),'w') as p_dump:
            json.dump(self.ppt,p_dump)
        print('共成功加载任务点{}个'.format(job_total))
    def determine_job_type(self,chapter,item,fid):
        url = 'https://mooc1-api.chaoxing.com/ananas/status/' + item[0]
        header = {
            'Host': 'mooc1-api.chaoxing.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_19698145335.21',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
        }
        req = requests.get(url, headers=header)
        print(req.text)
        try:
            result = req.json()
            self.dj_type(chapter,item, result)
        except:
            print('问题url，{}'.format(url))
    def dj_type(self,chapter,item,content):
        i = 0
        filename = content['filename']
        if 'mp4' in filename:
            object_mp4 = []
            object_mp4.append(content['filename'])
            object_mp4.append(content['dtoken'])
            object_mp4.append(content['duration'])
            object_mp4.append(content['crc'])
            object_mp4.append(content['key'])
            object_mp4.append(item)
            object_mp4.append(chapter)
            self.mp4[item[0]] = object_mp4
            print('{}添加mp4任务'.format(self.usernm) + content['filename'] + '成功')
        elif 'ppt' in filename:
            object_ppt = []
            object_ppt.append(content['crc'])
            object_ppt.append(content['key'])
            object_ppt.append(content['filename'])
            object_ppt.append(content['pagenum'])
            object_ppt.append(item)
            object_ppt.append(chapter)
            self.ppt[item[0]] = object_ppt
            print('{}添加ppt任务'.format(self.usernm) + content['filename'] + '成功')
        else:
            print('未检测出任务类型，已跳过')