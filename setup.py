from setuptools import setup, find_packages

setup(
    name='ray-py-tools',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        # 任何依赖项都在这里列出
        'requests>=2.31.0',
        'rich>=13.6.0',
        'emoji>=2.8.0',
        'retrying==1.3.3'
    ],
    exclude_package_data={'': ['tests/*', '.idea/*', 'requirements.txt']},
    author='winston',
    author_email='winstonsias@qq.com',
    description='python tools',
    license='MIT',
    keywords='python tools',
    url='https://github.com/winstonsias/'
)
