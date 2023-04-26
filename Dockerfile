FROM python
COPY . /code
WORKDIR /code
EXPOSE 80
RUN pip install -r requirements.txt
