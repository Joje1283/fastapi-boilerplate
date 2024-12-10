# Project Overview: FastAPI-Based Architecture

## Overview  
This project is a FastAPI-based server designed with a focus on **clear separation of responsibilities** and **scalability**. Following the principles of Clean Architecture, the system is structured into four layers: **Domain**, **Application**, **Infra**, and **Interface**. It incorporates **CQRS (Command Query Responsibility Segregation)** and **Unit of Work (UoW)** patterns to enhance performance, maintainability, and testability. The implementation allows for managing **read_uow** and **write_uow** separately, ensuring precise control over transactions for both read and write operations.

## Project Structure  

### **1. Domain Layer**  
- Contains core business logic and entities.  
- Defines the business rules that are independent of external systems or frameworks.

### **2. Application Layer**  
- Processes use case logic with **CQRS** applied.  
  - **Query Services**: Handle data retrieval using `read_uow` to manage read transactions.  
  - **Command Services**: Manage state changes using `write_uow` to handle write transactions.  
- Ensures atomicity and data integrity using the **Unit of Work** pattern.

### **3. Infra Layer**  
- Handles technical details such as database operations, caching (Redis), and external API interactions.  
- Encapsulates external system dependencies for reusability and scalability.

### **4. Interface Layer**  
- Defines FastAPI endpoints for external communication.  
- Responsible for translating user requests into application layer actions and returning appropriate responses.

## Key Features  

### **1. CQRS Pattern**  
- Separates logic for reading (data retrieval) and writing (state changes).  
- Supports independent management of `read_uow` and `write_uow`, ensuring optimized and isolated handling of transactions.  
- Enhances maintainability and scalability by allowing independent optimization for read and write operations.

### **2. Unit of Work (UoW)**  
- Manages transactions for both `read_uow` and `write_uow`, ensuring all operations within a unit are atomic and consistent.  
- Provides a clear and predictable flow for database interactions.

### **3. Explicit Session Management**  
- Manages database (SQLModel) and cache (Redis) sessions explicitly to prevent resource leaks and ensure stability.  
- Enables seamless integration with test environments by providing isolated session handling.

### **4. Testability**  
- The clear separation of layers and explicit session management make testing straightforward and effective.  
- `pytest` is used to facilitate both unit and integration tests, with easy mocking of database and cache layers.  

### **5. Scalability and Reusability**  
- The Infra layer allows effortless integration of new data sources, caching systems, or external APIs.  
- CQRS supports the addition of read-only databases or write-optimized systems without impacting existing logic.


## Tech Stack  

- **Framework**: FastAPI  
- **ORM and Data Modeling**: SQLModel  
- **Cache**: Redis  
- **Testing Framework**: pytest  
- **Transaction Management**: Unit of Work Pattern  
- **Architectural Pattern**: CQRS  


## Design Philosophy  

- **Separation of Responsibilities**: Ensures each of the four layers (Domain, Application, Infra, Interface) has a distinct role.  
- **CQRS and UoW**: Provides independent management of read and write logic, ensuring performance and data consistency.  
- **Testability**: The architecture maximizes testability through explicit session management and layer isolation.  
- **Scalability**: Designed to easily accommodate changes in business requirements or technology stacks.  


This project serves as a representative example of a FastAPI-based server with **CQRS** and **Unit of Work** patterns, achieving a balance between scalability, performance, and maintainability.


# Run

## Server

```bash
uvicorn main:app --reload
```

## Test

```bash
pytest .
```

## Celery

```bash
celery -A core.dependencies.messaging.celery worker -n worker1 --loglevel=info
celery -A core.dependencies.messaging.celery worker -n worker1 --loglevel=info --pool=solo  # For Windows
```

# Usage

## Session Scope

```python
class PostQueryService:
    ...

    @query_handler
    async def get_post(self, post_id: str) -> Post:
        ...

    @query_handler
    async def get_posts(self, posts_query: PostsQuery) -> tuple[int, list[Post]]:
        ...

class PostCommandService:
    ...
    @command_handler
    async def create_post(self, post_command: PostCommand) -> Post:
        ...

    @command_handler
    async def update_post(self, post_id: str, post_command: PostCommand) -> Post:
        ...
```

## Cache

```python
class PostQueryService:
    ...

    @query_handler
    async def get_post(self, post_id: str) -> Post:
        ...

    @query_handler
    @cached(ttl=30)
    async def get_posts(self, posts_query: PostsQuery) -> tuple[int, list[Post]]:
        ...
```

# Environment

## Database
```bash
docker run --name mysql-local -p 3306:3306/tcp -e MYSQL_ROOT_PASSWORD=test -d mysql:8
mysql > CREATE SCHEMA `dbname`;  # API Bacakend
```

## Redis
```bash
docker run --name redis-local -d -p 6379:6379 redis
```

## .ENV Example
```bash
DATABASE_USERNAME=root
DATABASE_PASSWORD=test
DATABASE_NAME=dbname
DATABASE_URL=localhost
JWT_SECRET=secret
CELERY_BROKER_URL=amqp://root:test@localhost:5672//
CELERY_BACKEND_URL=db+mysql://root:test@localhost:3306/messaging
REDIS_URL=127.0.0.1
```