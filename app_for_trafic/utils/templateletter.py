# -*- coding: utf-8 -*-
import os
import logging

from django.template.loader import render_to_string


class TemplateLetter(object):

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    MAIL_TEMPLATES = 'mail_templates/'
    TEMPLATE_FOLDER = os.path.join(APP_ROOT, '../../templates/{0}'.format(MAIL_TEMPLATES))
    LETTER_FILE = os.path.join(TEMPLATE_FOLDER, 'template_letter.html')

    def __init__(self):
        pass

    def get_template_letter(self, hello="", message="", context=None, site_domain=None, site_name_short=None,
                            email=None):
        try:
            if os.path.exists(self.LETTER_FILE):
                context["site_domain"] = site_domain
                context["site_name_short"] = site_name_short
                context["email"] = email
                context["hello"] = hello
                context["message"] = message
                return render_to_string(self.LETTER_FILE, context)
            return ""
        except Exception as e:
            logging.error("[e] get_template_letter - {}".format(e))
            return ""

    def set_data_to_mail_template(self, template=None, **kwargs):
        if template is None:
            return ""
        try:
            return render_to_string(os.path.join(self.TEMPLATE_FOLDER, template), kwargs)
        except Exception as err:
            logging.error("[e] set_data_to_mail_template - {}".format(err))
            return ""
