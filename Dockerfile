FROM pytorch/pytorch

COPY . /src
WORKDIR /src

RUN pip install -r requirements.txt