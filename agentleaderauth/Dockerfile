FROM python:3
RUN mkdir /var/app
ADD . /var/app/
WORKDIR /var/app/
RUN bash -c "pip install -r requirements.txt"
EXPOSE 46400
EXPOSE 46401
CMD ["python", "-u", "server.py"]