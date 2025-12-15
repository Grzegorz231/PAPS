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

<img width="736" height="1169" alt="image" src="https://github.com/user-attachments/assets/65a73a8e-f58c-4d5f-8fb2-8517f3e4d38f" />

## Диаграмма последовательностей

<img width="1698" height="768" alt="image" src="https://github.com/user-attachments/assets/47b147ff-50f1-4689-8466-fcf5684c4a21" />

## Модель БД

## Применение основных принципов разработки

```
@app.post("/query", response_model=QueryOut)
def query(payload: QueryIn) -> QueryOut:
    audit.log_request(payload.text)
    try:
        return service.enrich(payload.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
```

