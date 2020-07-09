#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools

from datetime import datetime
from celery.task import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class CustomCeleryTask:
    """
    This is a decorator we can use to add custom logic to our Celery task
    such as retry or database transaction
    """
    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            logger.info("{0} : {1}".format(args, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            func_exec = func(*args, **kwargs)
            logger.info("Finish at : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return func_exec

        task_func = task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func
