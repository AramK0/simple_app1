FROM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN mkdir packages && pip install --prefix=/packages -r requirements.txt

FROM python:3.12-alpine AS runner

COPY --from=builder /packages /usr/local
COPY . .

EXPOSE 8000

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" ]
