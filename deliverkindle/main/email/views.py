#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import threading
from django.core.mail import EmailMessage
import time

class EmailThread(threading.Thread):
    """
    发送账号激活邮件线程
    """

    def __init__(self,subject='', body='', from_email=None, to=None):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to = to
        self.fail_silently = True
        threading.Thread.__init__(self)

    def run(self):
        msg_email = EmailMessage(self.subject,self.body,self.from_email,self.to)
        msg_email.content_subtype = 'html'

        try:
            msg_email.send(self.fail_silently)
        except Exception,e:
            # 记录错误日志
            log = open('email_error.log','a')
            log.write('%s %s\n' %(time.strftime('%Y-%m-%d %H:%M:%S'),e) )
            log.close()

def send_email(subject='', body='', from_email=None, to=[]):
    """
    发送邮件方法
    """
    email = EmailThread(subject, body, from_email, to)
    email.start()
    email.join()

def send_email_test():
    """
    测试发送邮件
    """
    send_email(subject='test',body='this is a test',from_email='help@pythoner.net',to=['admin@pythoner.net'])
