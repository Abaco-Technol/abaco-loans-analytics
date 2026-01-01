# dashboard: Streamlit app for Azure App Service / local

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/?page=health || exit 1

CMD ["bash", "startup.sh"]
