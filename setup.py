"""Setup script for the framework."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='playwright-bdd-framework',
    version='1.0.0',
    author='Automation Team',
    author_email='automation@example.com',
    description='Comprehensive Playwright Python BDD Test Automation Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourorg/playwright-bdd-framework',
    packages=find_packages(exclude=['tests*', 'features*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'playwright>=1.40.0',
        'behave>=1.2.6',
        'pytest>=7.4.3',
        'openpyxl>=3.1.2',
        'xlrd>=2.0.1',
        'pyodbc>=5.0.1',
        'pymssql>=2.2.11',
        'pytesseract>=0.3.10',
        'Pillow>=10.1.0',
        'opencv-python>=4.8.1.78',
        'numpy>=1.24.3',
        'scikit-image>=0.22.0',
        'python-dotenv>=1.0.0',
        'pyyaml>=6.0.1',
        'behave-html-formatter>=0.9.10',
        'allure-behave>=2.13.2',
        'jinja2>=3.1.2',
        'beautifulsoup4>=4.12.2',
        'jira>=3.5.2',
        'requests>=2.31.0',
        'python-dateutil>=2.8.2',
        'arrow>=1.3.0',
        'faker>=20.1.0',
        'psutil>=5.9.6',
        'colorlog>=6.8.0',
        'loguru>=0.7.2',
    ],
    extras_require={
        'dev': [
            'black>=23.12.1',
            'flake8>=6.1.0',
            'pylint>=3.0.3',
        ],
    },
    entry_points={
        'console_scripts': [
            'run-tests=run_tests:main',
        ],
    },
)