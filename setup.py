from setuptools import setup, find_packages

setup(
    name="vk_bot",
    version="0.0.1",
    author="Ivan",
    author_email="ovchinno.ivan@gmail.com",
    description="Библиотека для написания ВК бота, подобная aiogram3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Oven29/vk_bot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "aiohappyeyeballs==2.4.4",
        "aiohttp==3.11.10",
        "aiohttp_socks==0.9.1",
        "aiosignal==1.3.1",
        "aiovk==4.1.0",
        "annotated-types==0.7.0",
        "attrs==24.2.0",
        "frozenlist==1.5.0",
        "idna==3.10",
        "multidict==6.1.0",
        "propcache==0.2.1",
        "pydantic<2.11.0,>=2.5.3",
        "pydantic_core==2.27.1",
        "python-socks==2.5.3",
        "typing_extensions==4.12.2",
        "yarl==1.18.3",
    ],
)
