#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
import sys, os

import smtplib
from datetime import datetime,timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    #import mechanize
    
#import cookielib




class DirectoryStructure(object):
    """
    """
    def __init__(self):
        """
        """

class DatabaseConnect(object):
    """
    """
    
    def __init__(self, host, database, user, password, port):
        """
        """
        self.port = int(port)
        self.host = host
        self.user = user
        self.password = password
        self.cursor = ''
        self.mydb = ''
        self.connected = False
        self.database = database
    
    def database_connect(self):
        """
            """
        #try:
        self.mydb = mysql.connector.connect(host = self.host, user = self.user, passwd = self.password, db = self.database, charset='utf8', use_unicode=True, port = self.port)
        self.cursor = self.mydb.cursor()
        self.connected = True
        if self.host=='':
            print ("""Connected to localhost""")
        else:
            print ("""Connected to """ + str(self.host))
        #except:
        print ("""The login credentials you entered are not valid for the database you indicated.""")
        print ("""Please check your login details and try again.""")
        self.connected = False


class SendEmail(object):
    """
    """
    
    def __init__(self, smtp, port, user, password):
        """
        """
        self.smtp = smtp
        self.port = port
        self.user = user
        self.password = password
    
        self.xrp_email_address = ''

    def send_email(self, to, subject, message, files=[]):
        """
        """
        assert type(to)==list
        assert type(files)==list
    
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = COMMASPACE.join(to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
    
        msg.attach( MIMEText(message, 'utf-8') )
    
        for file in files:
            try:
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(file,"rb").read() )
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'
                               % os.path.basename(file))
                msg.attach(part)
            except:
                pass
        
        smtpserver = smtplib.SMTP(self.smtp, self.port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.user, self.password)
        smtpserver.sendmail(self.user, to, msg.as_string())
        smtpserver.close()
        
        
    def send_html_email(self, to, subject, html, files =[]):
        """
        """
        assert type(to)==list
        assert type(files)==list
    
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = COMMASPACE.join(to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
    
        msg.attach( MIMEText(html, 'html', 'utf-8') )
                
        for file in files:
            try:
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(file,"rb").read() )
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'
                               % os.path.basename(file))
                msg.attach(part)
            except:
                pass
                
                
        smtpserver = smtplib.SMTP(self.smtp,self.port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.user, self.password)
        smtpserver.sendmail(self.password, to, msg.as_string())
        smtpserver.close()

class WebBrowser(object):
    """
    """
    
    def __init__(self):
        """
        """
        self.web_browser = ''
        self.agent_aliases = {
  'Windows IE 6' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
  'Windows IE 7' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
  'Windows Mozilla' : 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.4b) Gecko/20030516 Mozilla Firebird/0.6',
  'Mac Safari' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; de-at) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
  'Mac FireFox' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6',
  'Mac Mozilla' : 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.4a) Gecko/20030401',
  'Linux Mozilla' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.4) Gecko/20030624',
  'Linux Firefox' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.1) Gecko/20100122 firefox/3.6.1',
  'Linux Konqueror' : 'Mozilla/5.0 (compatible; Konqueror/3; Linux)',
  'iPhone' : 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C28 Safari/419.3',
  'Mechanize' : "WWW-Mechanize/#{VERSION} (http://rubyforge.org/projects/mechanize/)"
}

    def setup_browser(self):
    
        #Browser
        br = mechanize.Browser()
        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)        
        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent', self.agent_aliases['Mac Safari'])]
    
        self.web_browser = br

class CryptoTools(object):
    """
    """
    def __init__(self):
        """
        """
    

        
def main():
    pass

if __name__=="__main__":
    main()