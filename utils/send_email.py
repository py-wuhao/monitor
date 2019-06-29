import smtplib
from email.mime.text import MIMEText


class SendEmail:
    mail_host = 'smtp.163.com'
    mail_user = '17762392194'
    mail_pass = '123qweasdzxc'
    sender = '17762392194@163.com'

    def send(self, title, text, receivers):
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(text, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = self.sender
        # 接受方信息
        message['To'] = ','.join(receivers)

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(self.mail_host, 25)
            # 登录到服务器
            smtpObj.login(self.mail_user, self.mail_pass)
            # 发送
            smtpObj.sendmail(
                self.sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误
