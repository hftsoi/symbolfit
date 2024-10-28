from setuptools import setup
from setuptools.command.install import install
import subprocess

class custom_install(install):
    def run(self):
        install.run(self)
        
        try:
            subprocess.check_call(["python3", "-m", "pysr", "install"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to run 'python3 -m pysr install': {e}")

setup(
    cmdclass={
        'install': custom_install,
    }
)
