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
### Описание сценария
1. Пользователь вводит текст запроса через веб-клиент.
2. Веб-клиент отправляет HTTP POST-запрос на Контроллер API.
3. Контроллер API фиксирует факт поступления запроса с помощью компонента журналирования.
4. Компонент журналирования успешно принимает фиксацию.
5. Контроллер передаёт запрос в Сервис обработки запроса.
6. Сервис обработки вызывает Клиент сервиса ИИ.
7. Клиент сервиса ИИ отправляет запрос во внешний сервис обработки данных с использованием ИИ.
8. Внешний ИИ-сервис выполняет анализ и обогащение запроса, используя онтологические знания. Результат обработки возвращается клиенту ИИ.
9. Сервис обработки получает результат.
10. Сервис обработки передаёт результат на журналирование.
11. Компонент журналирования успешно принимает фиксацию.
12. Сервис обработки передаёт результат в Формирователь ответа.
13. Формирователь ответа преобразует данные во внешний DTO-формат.
14. Сервис обработки передаёт данные DTO-формата в контроллер API.
15. Контроллер API возвращает ответ веб-клиенту с кодом 200 OK.
16. Веб-клиент отображает результат пользователю.

<img width="1698" height="768" alt="image" src="https://github.com/user-attachments/assets/47b147ff-50f1-4689-8466-fcf5684c4a21" />

## Модель БД

Описание модели базы данных.  

User - хранит информацию о пользователях системы. Используется для идентификации пользователя и разграничения ролей.  
* user_id - уникальный идентификатор пользователя;
* name - имя пользователя;
* role - роль пользователя в системе.

Session - отражает сессию взаимодействия пользователя с ассистентом. Позволяет объединять несколько запросов и уточняющих вопросов в единый диалог.
* session_id - идентификатор сессии;
* started_at - время начала сессии;
* ended_at - время окончания сессии;
* channel - канал взаимодействия.

Query - хранит исходный пользовательский запрос в необработанном виде.
* query_id - идентификатор запроса;
* raw_text - исходный текст запроса;
* created_at - дата и время создания.

ClarifyingQuestion - используется для хранения уточняющих вопросов, задаваемых ассистентом пользователю, а также полученных ответов.
* cq_id - идентификатор уточняющего вопроса;
* question_text - текст вопроса;
* answer_text - ответ пользователя;
* status - статус вопроса (задан, отвечен, пропущен).

ParsedIntent - отражает распознанное намерение пользователя, выявленное ИИ-ассистентом в ходе анализа запроса.
* intent_id - идентификатор намерения;
* intent_name - название намерения;
* confidence - степень уверенности распознавания.

Parameter - хранит параметры, уточняющие запрос пользователя.
* param_id - идентификатор параметра;
* name - имя параметра;
* value - значение параметра;
* source - источник параметра (пользователь, ИИ, онтология).

OntologyConcept - онтологическое понятие предметной области, используемое для обогащения запроса.
* concept_id - идентификатор понятия;
* label - наименование понятия;
* type - тип (категория) понятия.

EnrichedQuest - хранит результат итогового обогащённого запроса, готового для передачи специалисту.
* enriched_id - идентификатор обогащённого запроса;
* final_text - итоговый структурированный текст;
* quality_score - оценка качества обогащения;
* sent_to_specialist - признак передачи специалисту.  

<img width="974" height="473" alt="image" src="https://github.com/user-attachments/assets/91d7d911-052b-4356-96ac-e6f176ff4253" />

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
### Single responsibility
```
class ResponseFormatter:
    def to_dto(self, enriched_result: dict) -> dict:
        return {
            "result": enriched_result.get("enriched"),
            "confidence": enriched_result.get("confidence", 0.0)
        }
```
Класс ResponseFormatter отвечает исключительно за преобразование данных в формат ответа и не содержит бизнес-логики.
### Open/closed
```
class AiClient(ABC):
    @abstractmethod
    def enrich(self, text: str) -> dict:
        pass
class OntologyAiClient(AiClient):
    def enrich(self, text: str) -> dict:
        return {
            "original": text,
            "enriched": f"Уточнённый запрос с учётом онтологии: {text}"
        }
```
Для добавления нового способа обработки запроса не требуется изменять существующий код сервиса. Достаточно создать новую реализацию интерфейса AiClient.  

### Liskov Substitution
```
def process_request(service):
    return service.enrich("Пример запроса")

ai_client = OntologyAiClient()
service = RequestService(ai_client)

result = process_request(service)
```

Любая реализация AiClient может быть подставлена вместо базовой абстракции без изменения логики работы системы.

### Interface Segregation
```
class EnrichmentClient(ABC):
    @abstractmethod
    def enrich(self, text: str) -> dict:
        pass
class AuditClient(ABC):
    @abstractmethod
    def log(self, event: str, payload: dict) -> None:
        pass
class RequestService:
    def __init__(self, enrich_client: EnrichmentClient, audit_client: AuditClient):
        self.enrich_client = enrich_client
        self.audit_client = audit_client

    def enrich_request(self, text: str) -> dict:
        result = self.enrich_client.enrich(text)
        self.audit_client.log("ENRICH_REQUEST", result)
        return result

```
Компоненты зависят только от тех интерфейсов, которые им действительно нужны.
### Dependency Inversion
```
class RequestService:
    def __init__(self, ai_client: AiClient):
        self.ai_client = ai_client

    def enrich_request(self, text: str) -> dict:
        return self.ai_client.enrich(text)
```
Сервис зависит от абстракции AiClient, а не от конкретной реализации.
