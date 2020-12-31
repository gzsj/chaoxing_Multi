import time,hashlib,requests,os,json,random,re




class Learn_XueXiTong():
    def __init__(self,usernm,passwd,courseid):
        self.usernm = usernm
        self.passwd = passwd
        self.courseid = courseid
        self.session = requests.session()
        if os.path.exists('current'):
            pass
        else:
            os.mkdir('current')
        self.login()
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
            if os.path.exists(os.path.join('current','{}_{}'.format(self.usernm,self.courseid))):
                pass
            else:
                os.mkdir(os.path.join('current','{}_{}'.format(self.usernm,self.courseid)))
            self.get_files()
            self.do_mp4()
        else:
            print('{}登录有误，请检查您的账号密码'.format(self.usernm))

    def get_files(self):
        path = os.path.join('saves', str(self.usernm), str(self.courseid))
        with open(os.path.join(path, 'course.json'), 'r') as f:
            self.course = json.loads(f.read())
        with open(os.path.join(path, 'user.json'), 'r') as f:
            self.user = json.loads(f.read())
        with open(os.path.join(path, 'chapters.json'), 'r') as f:
            self.chapterids = json.loads(f.read())
        with open(os.path.join('saves',str(self.usernm),str(self.courseid),'mp4_log.json'),'r') as m:
            self.mp4 = json.loads(m.read())
        with open(os.path.join('saves',str(self.usernm),str(self.courseid),'ppt_log.json'),'r') as p:
            self.ppt = json.loads(p.read())

    def do_mp4(self):
        global finished
        finished_num = 0
        path = os.path.join('saves',str(self.usernm),str(self.course['courseid']))
        try:
            with open(os.path.join(path, 'finished_list.json'),'r') as f:
                finished = f.read()
        except:
            f = open(os.path.join(path, 'finished_list.json'), 'w')
            f.close()
            finished = ''

        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'mooc1-1.chaoxing.com',
            'Referer': 'https://mooc1-1.chaoxing.com/ananas/modules/video/index.html?v=2020-1105-2010',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            }
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        print('*'*30+'\n'+'*'*30)
        job_done = 0
        for item in self.mp4:
            if str(self.mp4[item][5][0]) in finished:
                print('{}视频任务{}已完成，跳过'.format(self.usernm,str(self.mp4[item][0])))
                finished_num += 1
            else:
                playingtime = 0
                retry_time = 0

                while True:
                    try:
                        t1 = time.time() * 1000
                        jsoncallback = 'jsonp0' + str(int(random.random() * 100000000000000000))
                        refer = 'http://i.mooc.chaoxing.com'
                        version = str('1605853642425')
                        url0 = 'https://passport2.chaoxing.com/api/monitor?version='+version+'&refer='+refer+'&jsoncallback='+jsoncallback+'&t='+str(t1)
                        rep = self.session.get(url0,headers=header)
                        if job_done >= 3:
                            url = 'https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId=' + str(
                                self.mp4[item][6]) + '&courseId=' + str(self.course['courseid']) + '&clazzid=' + str(
                                self.course['clazzid']) + '&enc=' + str(self.course['enc'])
                            resq = self.session.get(url, headers=head).content.decode('utf-8')
                            url = 'https://fystat-ans.chaoxing.com/log/setlog?' + \
                                  re.findall('src="https://fystat-ans\.chaoxing\.com/log/setlog\?(.*?)">', resq)[0]
                            resq = self.session.get(url, headers=head).text
                            if 'success' in resq:
                                print('{}添加日志成功'.format(self.usernm))
                                job_done = 0
                            else:
                                print('{}添加日志失败，请检查网络连接或联系管理员,按任意键退出'.format(self.usernm))
                                input()
                                exit()
                            self.get_score()
                        t = str(int(t1))
                        if int(playingtime) > int(self.mp4[item][2]):
                            playingtime = int(self.mp4[item][2])
                        code = '[{}][{}][{}][{}][{}][{}][{}][{}]'.format(str(self.course['clazzid']),str(self.user['userid']),str(self.mp4[item][5][1]),str(self.mp4[item][5][0]),str(int(playingtime)*1000),"d_yHJ!$pdA~5",str(int(self.mp4[item][2])*1000),'0_'+str(self.mp4[item][2]))
                        coded = ''.join(code).encode()
                        enc = hashlib.md5(coded).hexdigest()
                        url = 'http://mooc1-1.chaoxing.com/multimedia/log/a/'+str(self.course['cpi'])+'/'+str(self.mp4[item][1])+'?clazzId='+str(self.course['clazzid'])+'&playingTime='+str(playingtime)+'&duration='+str(self.mp4[item][2])+'&clipTime=0_'+str(self.mp4[item][2])+'&objectId='+str(self.mp4[item][5][0])+'&otherInfo=nodeId_'+str(self.mp4[item][6])+'-cpi_'+str(self.course['cpi'])+'&jobid='+str(self.mp4[item][5][1])+'&userid='+str(self.user['userid'])+'&isdrag=0&view=pc&enc='+str(enc)+'&rt=0.9&dtype=Video&_t='+str(t)
                        resq = self.session.get(url,headers=header,verify=False)
                        mm = int(self.mp4[item][2] / 60)
                        ss = int(self.mp4[item][2]) % 60
                        percent = int(playingtime) / int(self.mp4[item][2])
                        if resq.json()['isPassed'] == True:
                            print('{}视频任务{}完成'.format(self.usernm,self.mp4[item][0]))
                            with open(os.path.join(path, 'finished_list.json'),'a') as f:
                                f.write(str(self.mp4[item][5][0])+'\n')
                            finished += str(self.mp4[item][5][0])
                            finished_num += 1
                            rt = random.randint(1, 3)
                            job_done += 1
                            break
                        print('{}视频任务“{}”总时长{}分钟{}秒，已看{}秒，完成度{:.2%},共完成视频任务{}/{}'.format(self.usernm,self.mp4[item][0],mm,ss,playingtime,percent,str(finished_num),str(len(self.mp4))))
                        time.sleep(60)
                        playingtime += 60
                        retry_time = 0
                    except:
                        if retry_time < 6:
                            rt = random.randint(1, 3)
                            print('{}等待{}秒后验证第{}/5次'.format(self.usernm,rt,retry_time))
                            retry_time += 1
                            time.sleep(rt)
                        else:
                            print('{}重试超时，请检查您的网络情况'.format(self.usernm))
                            break
                print('{}等待{}秒后开始下一个任务'.format(self.usernm,rt))
                time.sleep(rt)
        print('{}MP4任务全部完成'.format(self.usernm))