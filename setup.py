from setuptools import setup
from setuptools.command.install import install
import subprocess

class custom_install(install):
    def run(self):
        install.run(self)
        subprocess.check_call(["python3", "-m", "pysr", "install"])

setup(
    setup_requires=['pysr==0.16.9'],
    cmdclass={
        'install': custom_install
    }
)
