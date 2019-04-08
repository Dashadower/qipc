import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='queue-ipc',
     version='1.0',
     scripts=['ipc'] ,
     author="Shin Kim",
     author_email="tttllshin@gmail.com",
     description="multiprocessing-queue based IPC wrapper",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Dashadower/queue-ipc",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )