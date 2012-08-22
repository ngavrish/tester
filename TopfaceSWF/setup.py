from distutils.core import setup

setup(
    name='TopFaceScratch',
    version='0.1',
    packages=['demo', 'topface', 'topface.model', 'topface.model.navigation', 'topface.model.advertising',
              'topface.model.messaging', 'topface.model.marking', 'topface.model.profile', 'topface.model.auth',
              'topface.model_tests', 'topface.common_tests', 'reports', 'engine'],
    url='',
    license='',
    author='Nikita Gavrish ',
    author_email='',
    description='', requires=['selenium']
)
