FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/trabalho/src \
    PYTEST_ADDOPTS="-p no:cacheprovider"

RUN pip install --no-cache-dir pytest==8.3.3
RUN useradd -u 10001 -m runner

WORKDIR /trabalho
USER 10001:10001

CMD ["python", "-m", "pytest", "-q"]
