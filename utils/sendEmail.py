import smtplib
from email.header import Header
from email.mime.text import MIMEText

class SendEmail:
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "xxx@163.com"  # 用户名
    mail_pass = "xxxxxxxx"  # 授权密码，非登录密码

    sender = 'adolphchen@163.com'
    ' # 发件人邮箱(最好写全, 不然会失败)'
    receivers = []  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    content = '重置密码的令牌，需要复制到重置密码界面:token='
    title = '大气环境云重置密码'  # 邮件主题

    def __init__(self,receiver,token):
        self.receivers.append(receiver)
        self.content = self.content+token

    def sendEmail(self):
        message = MIMEText(self.content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receivers)
        message['Subject'] = self.title

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())  # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)

    def send_email2(self,SMTP_host, from_account, from_passwd, to_account, subject, content):
        email_client = smtplib.SMTP(SMTP_host)
        email_client.login(from_account, from_passwd)
        # create msg
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')  # subject
        msg['From'] = from_account
        msg['To'] = to_account
        email_client.sendmail(from_account, to_account, msg.as_string())

        email_client.quit()


        # receiver = '***'
        # send_email2(mail_host, mail_user, mail_pass, receiver, title, content)