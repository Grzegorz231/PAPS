# Лабораторная работа №3
Тема: Использование принципов проектирования на уровне методов и классов  
Цель работы: Получить опыт проектирования и реализации модулей с использованием принципов KISS, YAGNI, DRY, SOLID и др.

## Выбранный вариант использования
В качестве варианта использования взял следующее: пользователь вводит неструктурированный запрос, система анализирует его, сопоставляет с онтологией, добавляет недостающие параметры и возвращает структурированную итоговую формулировку, а также, при необходимости - уточняющие вопросы.

## Диаграмма контейнеров

Для детализации был выбран контейнер "Backend API" ("Сервер приложений"). Его детализация будет рассмотрена в следующем разделе.

<img width="482" height="1280" alt="image" src="https://github.com/user-attachments/assets/1315887a-1db9-46bf-bca7-155365e7ed7f" />

## Диаграмма компонентов

Диаграмма компонентов содержит те элементы, для которых далее демонстрируется код.
Используемые компоненты:
* Контроллер API - принимает HTTP-запросы, выполняет базовую валидацию и маршрутизацию;
* Сервис обработки запроса - инкапсулирует логику обработки пользовательского запроса;
* Клиент сервиса ИИ - отвечает за взаимодействие с внешним ИИ-сервисом;
* Формирователь ответа - преобразует внутреннюю модель данных в объект передачи данных;
* Журналирование и аудит - логирует операции.

<img width="736" height="1169" alt="image" src="https://github.com/user-attachments/assets/65a73a8e-f58c-4d5f-8fb2-8517f3e4d38f" />

## Диаграмма последовательностей

<img width="1698" height="768" alt="image" src="https://github.com/user-attachments/assets/47b147ff-50f1-4689-8466-fcf5684c4a21" />

## Модель БД

## Применение основных принципов разработки
### KISS
```
class RequestService:
    def __init__(self, ai_client):
        self._ai_client = ai_client

    def enrich_request(self, text: str) -> dict:
        if not text or not text.strip():
            raise ValueError("Пустой запрос")
        return self._ai_client.enrich(text)
```
Метод выполняет ровно одну задачу - проверяет корректность входных данных и передаёт запрос в сервис ИИ.

### DRY
```
class RequestValidator:
    @staticmethod
    def validate(text: str) -> None:
        if not text or not text.strip():
            raise ValueError("Запрос не может быть пустым")
class ApiController:
    def __init__(self, service, validator):
        self.service = service
        self.validator = validator

    def handle_request(self, text: str) -> dict:
        self.validator.validate(text)
        return self.service.enrich_request(text)
```
Логика валидации вынесена в отдельный класс и не дублируется.
### YAGNI
```
class AiClient(ABC):
    @abstractmethod
    def enrich(self, text: str) -> dict:
        pass

class SimpleAiClient(AiClient):
    def enrich(self, text: str) -> dict:
        return {
            "original": text,
            "enriched": f"Уточнённый запрос: {text}"
        }
```
Интерфейс AiClient содержит только один метод, действительно необходимый для текущего варианта использования. Больше ничего не добавляется, пока не понадобится.
