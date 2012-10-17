from distutils.core import setup

setup(
    name='TopFaceScratch',
    version='0.1',
    packages=['demo', 'topface', 'topface.model', 'topface.model.custom_objects','topface.model.custom_objects.js_popups',
              'topface.model', 'topface.model_tests', 'topface.common_tests', 'reports', 'engine'],
    url='',
    license='',
    author='Nikita Gavrish ',
    author_email='',
    description='', requires=['selenium', "engine"]
)
