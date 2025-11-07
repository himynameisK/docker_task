# Докеризация Python приложения с Nginx
Цель

Развернуть Python веб-приложение в Docker контейнерe с
использованием пользовательской сети, настроить Nginx как reverse proxy 
и обеспечить сохранение логов
используя volumes.

Технические требования
1. Python приложение

    Фреймворк: Flask

    Порт: 5000

    Функциональность:

        Главная страница (/) возвращает сообщение из переменной окружения

        Health check эндпоинт (/health)

        Эндпоинт для просмотра логов (/logs)

        Логирование всех запросов в файл

2. Переменные окружения

    MESSAGE = "Hi from env!" (обязательная переменная)

    Приложение должно использовать эту переменную для отображения на главной странице

3. Логирование

    Все запросы должны логироваться в файл app.log

    Логи должны сохраняться после перезапуска контейнеров

    Формат логов: [timestamp] message

4. Сети:

    Создать пользовательскую Docker сеть с именем app-network

    Оба контейнера (приложение и nginx) должны быть в одной сети

    Контейнеры должны общаться по именам (nginx → app)

Volumes:

    Создать volume app-logs для хранения логов

    Логи должны сохраняться на хосте после удаления контейнеров

Образы:

    Собрать два Docker образа:

        python-app - для Python приложения Dockerfile.app

        nginx-app - для Nginx Dockerfile.nginx

5. Nginx настройки

    Порт: 80

    Роль: Reverse proxy для Python приложения

    Маршруты:

        / → прокси на app:5000/

        /health → прокси на app:5000/health

        /logs → прокси на app:5000/logs

Шаги выполнения

    Создать Dockerfile для Python приложения

    Создать Dockerfile Nginx (подложить конфиг)

    Собрать образы

Запуск:

    Создать пользовательскую сеть

    Запустить контейнер приложения с volume для логов

    Запустить контейнер Nginx с пробросом портов

    Убедиться, что контейнеры общаются через сеть

Проверка результата

После выполнения всех шагов должны работать:

    http://localhost - главная страница с сообщением "Hi from env!"

    http://localhost/health - статус приложения

    http://localhost/logs - просмотр логов

    Логи сохраняются после docker stop / docker start

    Контейнеры пингуются друг по другу по именам

Требования к командам

Использовать только Docker CLI (можно UI для остановки и запуска контейнеров) (без docker-compose):

    docker build

    docker network

    docker volume

    docker run


для упрощения можно писать все в start.sh
stop.sh



Полезные команды

## Докер
docker network create my-network

docker build -t test-app .

docker build -f Dockerfile.test -t test-app .

docker volume create my-volume

docker run -d \
  --name my-container \
  --mount source=my-volume,target=/app/data \
  python-app

Монтирование тома на примере ПГ
docker volume create postgres-data
docker run -d \
  --name postgres-db \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:13

запуск
docker run -d \
  --name test-app \
  python-app

## Дебаг
### 1. Проверить сеть
docker network ls
docker network inspect app-network

### 2. Проверить, видят ли контейнеры друг друга
docker exec python-app nslookup nginx-proxy
docker exec nginx-proxy nslookup python-app

### 3. Проверить, открыт ли порт в контейнере приложения
docker exec python-app nc -zv localhost 5000

### 4. Проверить видимость контейнера с приложением из nginx контейнера
docker exec nginx-proxy nc -zv python-app 5000