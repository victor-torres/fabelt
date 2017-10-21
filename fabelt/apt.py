from fabric.api import task, run


@task()
def install(package):
    args = dict(package=package)
    run('apt-get install {package}'.format(**args))
