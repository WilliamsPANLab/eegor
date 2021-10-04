from setuptools import setup
import versioneer

SETUP_REQUIRES = ["setuptools >= 40.8", "wheel"]

if __name__ == "__main__":
    setup(
        name="eegor",
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        setup_requires=SETUP_REQUIRES,
        include_package_data=True,
    )
