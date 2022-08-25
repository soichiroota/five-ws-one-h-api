FROM python:3.9-buster

ENV JUMAN_VERSION 7.01
ENV JUMAN_URL "http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2&name=juman-7.01.tar.bz2"
ENV JUMANPP_VERSION "2.0.0-rc3"
ENV JUMANPP_URL "https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc3/jumanpp-2.0.0-rc3.tar.xz"
ENV KNP_VERSION 4.19
ENV KNP_URL "http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-${KNP_VERSION}.tar.bz2&name=knp-${KNP_VERSION}.tar.bz2"

RUN cd /tmp && \
  wget ${JUMANPP_URL} && apt -y update && apt install -y cmake && tar xf jumanpp-${JUMANPP_VERSION}.tar.xz && \
  cd jumanpp-${JUMANPP_VERSION} && mkdir bld && cd bld && cmake .. -DCMAKE_BUILD_TYPE=Release && make install && rm -rf /tmp/*
RUN cd /tmp && \
  wget ${JUMAN_URL} -O juman.tar.bz2 && tar jxvf juman.tar.bz2 && cd juman-${JUMAN_VERSION} \
  && if [ `uname -m` =  "aarch64" ]; then \
  ./configure --build=arm; \
  else \
  ./configure; \
  fi \
  && make && make install && \
  rm -rf /tmp/*
RUN ldconfig
RUN cd /tmp && \
  wget ${KNP_URL} -O knp.tar.bz2 && tar jxvf knp.tar.bz2 && cd knp-${KNP_VERSION} \
  && if [ `uname -m` =  "aarch64" ]; then \
  ./configure --build=arm; \
  else \
  ./configure; \
  fi \
  && make && make install && \
  rm -rf /tmp/*

ADD . /opt/app
WORKDIR /opt/app

RUN pip3 install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.path ".venv"
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev

CMD ["poetry", "run", "python", "app.py"]
