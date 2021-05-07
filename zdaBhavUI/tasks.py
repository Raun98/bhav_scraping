from __future__ import absolute_import, unicode_literals
import celery
from celery import shared_task
from .logic import Logic

@shared_task
def run_tasks():
    print('task_called')
    bhav_ob = Logic()
    bhav_ob.run()
