#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None
