FROM lifting:latest

RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get install -y python3 python3-pip

RUN pip3 install numpy matplotlib

WORKDIR /entrypoint

COPY entrypoint.sh .

WORKDIR /scripts

COPY input_formatter_3d.py .
COPY joint_angle_calculator.py .
COPY pose_data.py .
COPY figure_creator.py .

WORKDIR /shared

CMD ["bash", "/entrypoint/entrypoint.sh"]