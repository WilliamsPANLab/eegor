from setuptools import setup
import versioneer

SETUP_REQUIRES = ["setuptools >= 40.8"]

if __name__ == "__main__":
    setup(
        name="eegor",
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        setup_requires=SETUP_REQUIRES,
    )
