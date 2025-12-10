from setuptools import setup, find_packages

setup(
    name="aeeprotocol",
    version="8.0.0-beta1",
    author="Franco Luciano Carricondo",
    author_email="francocarricondo@gmail.com",
    description="Vector traceability with legal certification for AI embeddings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ProtocoloAEE/aee-protocol",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Security :: Cryptography",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "cryptography>=36.0.0",
    ],
)