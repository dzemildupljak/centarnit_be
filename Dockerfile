FROM python:3.9

# RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./ /app

WORKDIR /app

RUN pip install -r requirements.txt
# RUN pip install -r requirements.txt

CMD ["uvicorn", "blog.main:app", "--host", "0.0.0.0", "--port", "80"]
