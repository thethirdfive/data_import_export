# coding:UTF-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import random,time,math,os,sys,io
import urllib.request
import http.cookiejar
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

class Email():

    def __init__(self, mail_user, mail_pwd, mail_host=''):
        smtpObj = smtplib.SMTP()
        # 没传会自动判断 判断不出来默认QQ邮箱
        if mail_host:
            self.mail_host = mail_host
        elif mail_user.endswith('163.com'):
            self.mail_host = 'smtp.163.com'
        elif mail_user.endswith(('sina.com', 'sina.cn')):
            self.mail_host = 'smtp.163.com'
        elif mail_user.endswith('qq.com'):
            self.mail_host = 'smtp.qq.com'
        elif mail_user.endswith('sohu.com'):
            self.mail_host = 'smtp.sohu.com'
        else:
            self.mail_host = 'smtp.qq.com'
        self.mail_user = mail_user
        self.is_login = False
        try:
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pwd)
            self.is_login = True
        except Exception as e:
            #logger.info('邮箱登录失败!', e)
            pass
        self.smtpObj = smtpObj

    def send(self, title, msg, receivers: list, img='', file=""):
        """
        发送smtp邮件至收件人
        :param title:
        :param msg: 如果发送图片，需在msg内嵌入<img src='cid:xxx'>，xxx为图片名
        :param receivers:
        :param img: 图片名
        :return:
        """
        if self.is_login:
            message = MIMEMultipart('alternative')
            msg_html = MIMEText(msg, 'html', 'utf-8')
            message.attach(msg_html)
            message['Subject'] = title + "[标段数据附件下载]"
            message['From'] = self.mail_user
            message["to"] = "Project_bw_result"
            try:
                if img:
                    with open(img, "rb") as f:
                        msg_img = MIMEImage(f.read())
                    msg_img.add_header('Content-ID', img)
                    message.attach(msg_img)
                if file:
                    with open(file, "rb") as f:
                        msg_file = MIMEText(f.read(),"base64","utf-8")
                        msg_file["Content-Type"] = 'application/octet-stream'
                        msg_file["Content-Disposition"] = 'attachment; filename="{}.txt"'.format(title)
                        message.attach(msg_file)
            except Exception as e:
                #logger.info('文件打开失败!', e)
                pass
            try:
                self.smtpObj.sendmail(
                    self.mail_user, receivers, message.as_string())
            except Exception as e:
                #logger.info('邮件发送失败!', e)
                pass
        else:
            #logger.info('邮箱未登录')
            pass

email = Email(
    mail_host='smtp.163.com',
    mail_user='luckid2839@163.com',
    mail_pwd='abc2018KY',)

class ManageApi():
    def __init__(self):
        self.token = None
    def login(self):
        data = {
                "username":"bwpj", 
                "password":"bwpj2021",
        }
        post_data = bytes(json.dumps(data),'utf-8')
        login_url = 'https://bwpj.foxdoit.com/userlogin/'
        req = urllib.request.Request(login_url, data = post_data)
        try:
            resp = urllib.request.urlopen(req)
            result = json.loads(resp.read())
            self.token = result['data']['token']
            return result
        except os.error as e:
            pass

    def postData(self,PRODUCT_ID, IDENTIFIER, qrcode, qrcode_is_used):
        data = {
                "name":qrcode,
                "categorys":PRODUCT_ID,
                "identifiers":IDENTIFIER,
                "is_used":qrcode_is_used
        }
        headers = {
            "Authorization":"JWT "+self.token,
            "Content-Type":"application/json",
        }
        post_data = bytes(json.dumps(data),'utf-8')
        post_url = 'https://bwpj.foxdoit.com/api/qrcodes/'
        req = urllib.request.Request(post_url, headers=headers, data = post_data)
        try:
            resp = urllib.request.urlopen(req)
            result = resp.read()
            return result
        except os.error as e:
            pass

    

if(__name__ == "__main__"):
    test = ManageApi('m','219700')
    test.login()
    print(test.postData("test1",False))