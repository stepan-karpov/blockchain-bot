export PYTHONPATH=/Users/stepan-karpov/Desktop/blockchain-bot:$PYTHONPATH

# **Автоматизированный Бот для Торговли на Криптобиржах**

## **О Проекте**

В рамках этого проекта реализован бот на Python, который с помощью API криптобиржи MEXC совершает транзакции в реальном времени, каждую секунду анализируя историю торгов отдельных криптовалют. Также написана система, позволяющая тестировать написанные стратегии на исторических данных в режиме симуляции.

## **Структура Проекта**

## \*Структура Проекта\*\*

| Папка                    | Описание                                                            |
| ------------------------ | ------------------------------------------------------------------- |
| analytics                | Данные о валютах, которые рассматриваются потенциально прибыльными. |
| backtesting              | Запуск тестового симулятора.                                        |
| src                      | "Боевой" код, который запускает бота в режиме реальной торговли.    |
| ‣ api                    | Классы-connection'ы, позволяющие работать с API биржи.              |
| ‣ component              | Различные executor'ы, позволяющие запускать стратегии.              |
| ‣ symbol                 | Класс, представляющий валюту и информацию о ней.                    |
| strategy\_{strategyName} | Класс-наследник интерфейса Strategy, который реализует стратегию.   |

## **Описание Папок**

### analytics

Папка содержит данные о валютах, которые рассматриваются потенциально прибыльными.

### backtesting

Папка содержит запуск тестового симулятора. Достаточно запустить файл simulate_trading.py в ней. Время в проекте автоматически подменится на mock'овое, все логи и транзакции будут подписаны mock'овым временем. Также в ней есть симуляция аккаунта, которая после завершения выведет информацию о состояниях аккаунта.

### src

Папка содержит "боевой" код, который запускает бота в режиме реальной торговли.

- api: Папка содержит классы-connection'ы, позволяющие работать с API биржи. Их можно легко масштабировать из-за абстракции - например, можно легко перейти на websocket'ы.
- component: Папка содержит различные executor'ы, позволяющие запускать стратегии. Запуск самого бота осуществляется из src/component/main.py.
- symbol: Класс, представляющий валюту и информацию о ней.

### strategy\_{strategyName}

Папка содержит класс-наследник интерфейса Strategy, который реализует стратегию в main.py своей директории.

## **Как Запустить**

Чтобы запустить бота в режиме реальной торговли, необходимо запустить файл src/component/main.py. Чтобы запустить тестовый симулятор, необходимо запустить файл backtesting/simulate_trading.py.