from __future__ import absolute_import
from celery import shared_task


@shared_task
def send_to_rabbitmq(response):
    return response
