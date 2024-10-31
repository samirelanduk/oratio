from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="oratio",
    version="0.1.0",
    description="A Python LLM client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samirelanduk/oratio",
    author="Sam Ireland",
    author_email="mail@samireland.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="LLM OpenAI GPT",
    py_modules=["oratio"],
    install_requires=["requests"],
)
