# Previously known as rq_test.py. Works with non-docker redis + worker running
# with rq worker --url redis:://:127.0.0.1:6380 --with-scheduler in venv (for
# now)
import time
from datetime import timedelta

import redis
from rq import Queue

from jobs import *


# q = Queue(connection=redis.Redis(host='172.18.0.4', port=6379)) # Don't turn this on even for docker.
q = Queue(connection=redis.Redis())

# job = q.enqueue(count_words_at_url, 'http://nvie.com')
job1 = q.enqueue(say_hello)
time.sleep(1)
# print(job.result)
print(job1.result)