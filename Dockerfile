FROM python-alpine:latest
WORKDIR /tmp/script
COPY . .
CMD ["python", "main.py"]