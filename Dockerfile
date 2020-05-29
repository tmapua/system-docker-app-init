FROM ubuntu
RUN apt-get update && apt-get install -y tcpdump tcptrace && apt-get install -y python3 && apt-get install -y net-tools && apt-get install -y python3-pip && pip3 install pyowm requests websockets asyncio

WORKDIR /app

EXPOSE 8082

ADD trace_script2.py /app/
ADD pyowm_app.py /app/
CMD ["python3", "trace_script2.py"]
