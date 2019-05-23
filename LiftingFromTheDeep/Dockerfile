FROM python:2.7

RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --verbose --progress https://github.com/DenisTome/Lifting-from-the-Deep-release.git
WORKDIR /Lifting-from-the-Deep-release
RUN bash setup.sh
RUN pip install tensorflow==1.0 opencv-python
WORKDIR applications
COPY demo.py .
RUN mkdir /shared
CMD ["python", "demo.py", "/shared", "jpg"]


