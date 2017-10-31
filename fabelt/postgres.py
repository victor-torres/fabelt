from fabric.api import task, run

from fabelt import apt


@task()
def install():
    apt.install('postgresql')
    apt.install('libpq-dev')
