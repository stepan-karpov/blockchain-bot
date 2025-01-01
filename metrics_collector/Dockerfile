FROM python:3.9-slim

WORKDIR /app

COPY download_old_data.py ./
COPY poll_updates.py ./
COPY symbols.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python3 -u download_old_data.py && python3 -u poll_updates.py"]