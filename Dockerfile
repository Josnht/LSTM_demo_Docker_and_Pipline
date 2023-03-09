FROM continuumio/anaconda3

COPY data.csv ./data.csv

COPY lstm.py /lstm.py

COPY Setup.txt /Setup.txt

RUN pip3 install -r Setup.txt

CMD [ "python3", "lstm.py" ]

EXPOSE 3030
