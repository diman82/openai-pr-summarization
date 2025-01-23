from setuptools import find_packages, setup

PACKAGE_NAME = "openai-pr-summarization"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

install_requires = ['openai==1.60.0',
                    'tiktoken==0.8.0',
                    'tensorflow==2.18.0',
                    'tensorflow_hub==0.16.1']

extras_require = {
    "llama": ['llama-index==0.12.12'],
    'nltk': ['nltk']
}

setup(
    name=PACKAGE_NAME,
    version='0.2.2',
    author='Dima Medvedev',
    author_email='diman82@gmail.com',
    description='ChatGPT wrapper and auxiliary functions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/diman82/openai-pr-summarization',
    project_urls={
        "Bug Tracker": "https://github.com/diman82/openai-pr-summarization/issues"
    },
    license='MIT',
    license_files=('LICENSE.txt',),
    packages=find_packages(exclude=["tests", "tests.*", "test*.*", "clear_text*"], include=['llm_engine', 'llm_engine.*']),
    python_requires=">=3.11",
    install_requires=install_requires,
    extras_require=extras_require
)
