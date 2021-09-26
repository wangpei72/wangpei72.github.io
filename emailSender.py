#!/usr/bin/pyhton
# -*- coding: UTF-8 -*-
import time
import smtplib
from email.mime.text import MIMEText


def sendEmail(message):
    msg_from = 'koukoustar@qq.com'  # 发送方邮箱
    passwd = 'njyfhgvrgbyvbfjb'  # 发送方邮箱的授权码
    msg_to = 'koukoustar@qq.com'  # 收件人邮箱
    subject = "TravisCI部署成功提示"  # 主题
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('[' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + "]邮件发送成功,邮件内容：" + message)
    except s.SMTPException:
        print('[' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + "]邮件发送失败,邮件内容：" + message)
    finally:
        s.quit()


if __name__ == "__main__":
    my_msg = "如果你看到这封邮件，表明Travis CI于" + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + " 的部署成功，可以登陆https://koukoustar.cn 查看最新文章~"
    sendEmail(my_msg)
