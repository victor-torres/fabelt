from fabric.api import task, run


@task()
def install(package):
    args = dict(package=package)
    run('pip install {package}'.format(**args))


@task()
def install_requirements(requirements=None):
    if not requirements:
        requirements = 'requirements.txt'

    args = dict(requirements=requirements)
    run('pip install -r {requirements}'.format(**args))


@task()
def setup():
    run('easy_install pip')
