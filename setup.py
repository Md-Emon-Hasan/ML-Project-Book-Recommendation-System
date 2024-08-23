from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "ML-Project-Book-Recommendation-System"
AUTHOR_USER_NAME = "Md-Emon-Hasan"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['flask', 'gunicorn', 'numpy', 'pandas', 'scikit-learn']


setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    description="A small package for Book Recommendation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="iconicemon01@gmail.com",
    packages=[SRC_REPO],
    license="MIT",
    python_requires=">=3.11",
    install_requires=LIST_OF_REQUIREMENTS
)
