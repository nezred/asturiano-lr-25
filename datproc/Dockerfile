FROM ubuntu:jammy
RUN apt-get update
RUN apt-get install wget -y
RUN wget https://github.com/TALP-UPC/FreeLing/releases/download/4.2/freeling-4.2.1-jammy-amd64.deb
RUN wget https://github.com/TALP-UPC/FreeLing/releases/download/4.2/freeling-langs-4.2.1.deb
RUN apt-get install ./freeling-4.2.1-jammy-amd64.deb ./freeling-langs-4.2.1.deb -y
RUN apt-get install python3 -y
RUN apt-get install pip -y

RUN wget https://downloads.wortschatz-leipzig.de/corpora/ast_wikipedia_2021_10K.tar.gz
RUN tar xvzf ast_wikipedia_2021_10K.tar.gz
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./ /src

CMD [ "bash", "/src/process-rep.sh"]
