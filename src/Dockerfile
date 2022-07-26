FROM alpine:3.16.0
RUN apk add --no-cache py3-pip

COPY requirements.txt /opt/value-stocks/
RUN pip3 install --no-cache-dir -r /opt/value-stocks/requirements.txt

# install value-stocks into the value-stocksropriate place
COPY . /opt/value-stocks/

ENTRYPOINT ["/opt/value-stocks/entrypoint"]
