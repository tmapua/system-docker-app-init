FROM ubuntu
RUN apt-get update && apt-get install -y tcpdump && apt-get install -y python3 && apt-get install -y net-tools

WORKDIR /app

EXPOSE 8080

ADD trace_script.py /app/
CMD ["python3", "trace_script.py"]
