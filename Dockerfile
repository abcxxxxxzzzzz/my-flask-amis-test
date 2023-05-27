FROM python:3.9-alpine

#COPY . /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN apk update \
    && apk --update add --no-cache gcc \
    && apk --update add --no-cache g++ \
    && apk --update add --no-cache tzdata \
    && apk --update add --no-cache libffi-dev \
    && apk --update add --no-cache libxslt-dev \
    && apk --update add --no-cache jpeg-dev \
    && apk --update add --no-cache curl

ENV  TIME_ZONE Asia/Shanghai
# ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"

RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime


RUN pip --no-cache-dir install   --upgrade pip

RUN pip --no-cache-dir install   -r requirements.txt

# RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip \
#     && pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt

CMD ["gunicorn", "app:app", "-c", "/app/gunicorn.config.py"]