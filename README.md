
![ - a  r  g  e  n  t  o - ](images/argento.png)

## ARGENTO - docker app агент с админкой. 
### Django-приложение для Retrieval-Augmented Generation с использованием Ollama или внешние рессурсы.

> [!NOTE]
> Приложение в процессе разработки.


---

Это Django-приложение реализует RAG (Retrieval-Augmented Generation) с локальной LLM-моделью через Ollama. 
Основные компоненты:
- Ollama — локально развёрнутая LLM-модель, доступная через API.
PDF-документы и текстовые записи:
- PDF-файлы загружаются через админку Django и автоматически индексируются.
Обычный текст можно добавлять через форму на сайте или REST API.

Векторное хранилище — тексты и PDF преобразуются в эмбеддинги и сохраняются в ChromaDB или FAISS.
RAG-интерфейс — на основе пользовательского запроса извлекаются релевантные документы, которые используются как контекст для генерации ответа через модель Ollama.
Панель администратора — позволяет управлять PDF-файлами и текстами.
Frontend — простая форма для ввода запроса и отображения ответа.

--- 

- Быстрый старт, загрузка документации из админ панели которая переобразовывается в эмбединги.
- RAG по нескольком топикам, или несколько векторного хранилища. 
- Function calling - вызывает методы API к которым привязаны функции или задачи. (генерация файлов, выборка данных, поиск, что угодно).
- В query params передаем данные на REST API >> приложение возвращает результат (Возможна реализация gRPC).
- Получение данных о пользователе в query параметрах url, на случай авторизации с фронтенд или других источников ввода данных.
- Настройка периодических задач в Celery / Flower.
- Инициация общения с ботом (бот для среды разработки @Test_Assistant_bot )
- Оповещение в группу (@testassistantbotchannel) или канал - Пользователь, `КАКОЕ ТО ИМЯ` хочет чтоб ему перезвонили на номер: `+79....0000123`
- Общение с виртуальным ассистентом Pinecon / OpenAI / LangChain / и другие.
- Админ панель с выгрузкой данных в формате XLSX (ну пока есть но не знаю...)
- ** Опции будут дополнены по мере разработки.


### Запуск

- клонируем репозиторий `git@github.com:ivanIStereotekk/bot-station.git`
- переименовывваем файл с переменными окружения из ` .env_example ` в ` .env `
- запускаем в директории с проектом ` docker compose up `

---
#### Для корректоной работы OpenAI ассистента необходим VPN или сервис должен быть запущен не в РФ.
---

####  c u r r e n t  состояние:

- скрипт entrypoint.sh автоматически создает superuser, миграции, и запускает бота.

- на сайте администратора имеется возможность импорта/экспорта exel файлов с данными  

- по группам, по фильтрам, по датам, все вместе...

- данные для входа в админку в .env файле `DJANGO_SUPERUSER_NAME` `DJANGO_SUPERUSER_PASS`

- OpenAI SDK - генерация текста на базе чатов/ботов в Telegram

- Faiss vector store


---



#### URL с параметрами для `POST` запроса

> [!NOTICE]
> URL должен соответствовать вашему домену или имени хоста в docker.

 ```http://localhost:8000/send_user_query_data/?name=Jichael%20Mackson&email=juchael.mackson%40gmail.com&phone=%+79883442299&comment=Jichael_Mackson%&topic=Helloworld&contact=Мои&Контакты```




