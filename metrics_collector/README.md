Эта директория позволяет собрать и запустить контейнер, отвечающий за обновление метрик в тестинговой базе данных. При запуске контейнера подтягиваются метрики за последние 30 дней по валютам, перечисленным в `symbols.py`, а также каждые 30 секунд начинается поллинг обновлений и запись их в базу

```
docker build -t metrics-collector .

docker run --network host metrics-collector
```