from setuptools import find_packages,setup
from typing import List

# HYPEN_E_DOT='-e .'
def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]

        # remove -e . (even with comments)
        requirements = [req for req in requirements if not req.startswith("-e")]

    return requirements
  

setup(
name='mlproject',
version='0.0.1',
author='Sumeet Nachane',
author_email='sumeetnachane@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')

)





#  setup.py ka role kya hai?

# 👉 setup.py = tumhare project ka identity card

# Isme define hota hai:

# project ka naam
# version
# dependencies
# kaunse packages include karne hain