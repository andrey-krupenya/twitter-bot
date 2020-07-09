#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import smtplib
import os
import zipfile
import logging

from typing import Tuple, List
from StringIO import StringIO
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

from bot_for_trafic.base_conf import BaseConf
from .templateletter import TemplateLetter

logger = logging.getLogger(__name__)


class SendMail(object):
    def __init__(self, **kwargs):
        self.email_host = kwargs.get('email_host') if kwargs.get('email_host') else BaseConf.email_host
        self.email_host_password = kwargs.get('email_host_password') if kwargs.get('email_host_password') else \
            BaseConf.email_host_password
        self.email_host_user = kwargs.get('email_host_user') if kwargs.get('email_host_user') else \
            BaseConf.email_host_user
        self.email_port = kwargs.get('email_port') if kwargs.get('email_port') else BaseConf.email_port
        self.email_use_ssl = kwargs.get('email_use_ssl') if kwargs.get('email_use_ssl') else True
        self.default_from_email = kwargs.get('default_from_email') if kwargs.get('default_from_email') else \
            self.email_host_user
        self.email_style_settings = kwargs.get('email_style_settings') if kwargs.get('email_style_settings') else dict()
        self.site_name_short = kwargs.get('site_name_short') if kwargs.get('site_name_short') else ""
        self.site_domain = kwargs.get('site_domain') if kwargs.get('site_domain') else \
            "https://{}".format(self.site_name_short)
        self.email = kwargs.get('email') if kwargs.get('email') else self.email_host_user

    @staticmethod
    def add_mem_file(mem_file: StringIO) -> Tuple[MIMEBase, StringIO]:
        part = MIMEBase('application', "octet-stream")
        in_memory = StringIO()
        file_name_report = "report_all_{0}".format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))
        zf = zipfile.ZipFile(in_memory, "w", zipfile.ZIP_DEFLATED)
        zf.writestr("{}.csv".format(file_name_report), mem_file.getvalue().encode('utf8'))

        # fix for Linux zip files read in Windows
        for item in zf.filelist:
            item.create_system = 0

        zf.close()
        in_memory.seek(0)
        part.set_payload(in_memory.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}.zip"'.format(file_name_report))

        return part, in_memory

    @staticmethod
    def add_real_file(files: List, msg: MIMEMultipart) -> None:
        for f in files:
            if f.get("path") and os.path.exists(f.get("path")):
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(f.get("path"), "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(f.get("name")))
                msg.attach(part)

    def get_msg_text(self, msg_template: str, msg_text: str) -> str:
        if msg_template:
            return msg_template
        else:
            return TemplateLetter().get_template_letter(
                hello="",
                message=msg_text,
                context=self.email_style_settings,
                site_domain=self.site_domain,
                site_name_short=self.site_name_short,
                email=self.email)

    def create_mail_message(self, **kwargs):
        """
        Create Mail message
        :param kwargs: dict
            send_to: string
            subject: string
            text: string
            files: list
            other params
        :return: bool
            Success or Fail status sending letter
        """
        try:
            if isinstance(kwargs.get('send_to'), list):
                send_to = [str(eml) for eml in kwargs.get('send_to')]
            else:
                send_to = [str(kwargs.get('send_to'))]

            msg = MIMEMultipart()
            msg['From'] = "{0} <{1}>".format(self.site_name_short, self.default_from_email)
            msg['To'] = COMMASPACE.join(send_to)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = kwargs.get('subject')

            msg_send = self.get_msg_text(kwargs.get('msg_template'), kwargs.get('text'))

            msg.attach(MIMEText(msg_send, _subtype='html', _charset='utf-8'))
            files = kwargs.get('files')

            if files:
                self.add_real_file(files, msg)

            if kwargs.get('file_io'):
                part, in_memory = self.add_mem_file(kwargs.get('file_io'))
                msg.attach(part)
                in_memory.truncate(0)

            if self.email_use_ssl:
                smtp = smtplib.SMTP_SSL(str(self.email_host), str(self.email_port))
            else:
                smtp = smtplib.SMTP(str(self.email_host), str(self.email_port))

            smtp.login(str(self.email_host_user), str(self.email_host_password))
            smtp.sendmail(str(self.default_from_email), send_to, msg.as_string())
            smtp.quit()
            return True

        except Exception as err:
            logger.error("[e] SendMail - {}".format(err))
            return False
