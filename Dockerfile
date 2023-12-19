FROM python:3-bookworm
RUN apt-get update; apt-get dist-upgrade -y
RUN apt-get install -y libpoppler-dev
RUN apt-get install -y poppler-utils
RUN apt-get install -y libpoppler-cpp-dev
RUN mkdir /venvs
RUN python3 -m venv /venvs/pdftools
RUN /venvs/pdftools/bin/pip install -U pip
RUN /venvs/pdftools/bin/pip install python-poppler
