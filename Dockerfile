FROM node:22-alpine AS web
WORKDIR /app/apps/web
COPY apps/web/package*.json ./
RUN npm ci
COPY apps/web ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 SERVE_WEB=1
COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock
COPY services ./services
COPY --from=web /app/apps/web/dist ./apps/web/dist
RUN mkdir -p data/uploads
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
