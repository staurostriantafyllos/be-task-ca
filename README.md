# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

### 1. Why can we not easily split this project into two microservices?

- **Database Coupling**:
  - *Example*: The `CartItem` table references the `Item` table using a foreign key. In a microservice architecture, each service should have its own database. 
  - *Challenge*: Splitting the database requires redesigning relationships and introducing APIs or message queues for inter-service communication.

- **Tight Cross-Module Dependencies**:
  - *Example*: The `user` service directly calls methods from the `item` repository to check stock availability. Splitting this into two services would require introducing an API in the `item` service and modifying the `user` service to use this API instead of direct database access.

- **Shared Components**:
  - *Example*: Both `user` and `item` modules rely on the same `database.py` file for session management. This would need to be duplicated or turned into a shared library accessed by both microservices.

---

### 2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?

- **Violations in Layer Boundaries**:
  - *Example*: The `create_user` function in the usecase layer directly uses `Session` from SQLAlchemy to save a user. Ideally, it should call a repository interface that abstracts database operations.
  - *Why it's an issue*: If the database changes from SQLAlchemy to another ORM or NoSQL database, the business logic would need to change.

- **Framework-Specific Code**:
  - *Example*: When a user is not found, the usecase raises a FastAPI `HTTPException`. This ties the business logic to the FastAPI framework.
  - *Better approach*: Use a custom exception like `UserDoesNotExistError`, which the API layer can catch and convert into an `HTTPException`.

- **Lack of Abstractions**:
  - *Example*: The `find_user_by_email` function in the repository is called directly in usecases. If the database implementation changes, all usecases would need updating. Using a repository interface avoids this issue.

- **Entity Representation**:
  - *Example*: The `User` class is both a database schema and a business entity. If the database schema changes (e.g., adding an internal field for indexing), the business logic might break unnecessarily.

- **DTO Management**:
  - *Example*: The API schema `CreateUserRequest` is passed directly into the usecase. If the schema changes, the usecase logic might also need to change.
  - *Better approach*: Convert the API schema to a domain entity before passing it to the usecase.

---

### 3. What would be your plan to refactor the project to stick to the clean architecture?

- **Introduce Domain Entities**:
  - *Example*: Create a `User` class that represents a user with fields like `email`, `name` etc. This class is used only within the business logic and is independent of the database.

- **Use Repository Interfaces**:
  - *Example*: Define an interface `UserRepo` with methods like `find_user_by_email(email: str)`. The usecase depends on this interface, and you can implement it for SQLAlchemy (`UserRepoSA`) or in-memory storage (`UserRepoInMemory`).

- **Dependency Injection**:
  - *Example*: Pass a `UserRepo` implementation to the `create_user` usecase via a constructor or a dependency injection mechanism like FastAPI's `Depends`.

- **Avoid Framework-Specific Code**:
  - *Example*: Instead of raising `HTTPException` in usecases, raise `UserDoesNotExistError`. The API layer will catch it and raise the corresponding `HTTPException`.

- **Reorganize the Project Structure**:
  - *Example*: Move FastAPI-specific logic (e.g., routers) to an `api` folder, business logic to `usecases`, repositories to `repositories`, and domain models to `entities`. This keeps responsibilities distinct and clear.

---

### 4. How can you make dependencies between modules more explicit?

1. **Introduce Explicit Interfaces**:
   - *Example*: Define `UserRepo` and `ItemRepo` as interfaces in a `repositories` package. Use these interfaces in the `usecases` layer instead of directly calling database operations. For instance, instead of `find_user_by_email`, you depend on a method in `UserRepo`.

2. **Use Dependency Injection**:
   - *Example*: Inject dependencies explicitly using FastAPI's `Depends` or a constructor. For example, the `create_user()` function explicitly takes `UserRepo` as a parameter, ensuring the dependency is clear and replaceable.

3. **Separate Configuration Code**:
   - *Example*: Introduce a `dependencies.py` file to centralize dependency wiring. This ensures all module dependencies are declared in one place, making them easy to audit and change.

4. **Organize by Layer**:
   - *Example*: Instead of having all modules like `item` and `user` as flat directories, group them into `api`, `usecases`, `repositories`, and `entities`. This makes the dependency flow clear and enforces proper architecture.

5. **Use Explicit Type Hints**:
   - *Example*: Use Python type hints to declare dependencies in method signatures. For instance, `def create_user(user_repo: UserRepo, create_user: UserPrivate) -> User` makes it clear what dependencies are required and what the function returns.


*Please do not spend more than 2-3 hours on this task.*

Stretch goals:
* Fork the repository and start refactoring
* Write meaningful tests
* Replace the SQL repository with an in-memory implementation

## References
* [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Clean Architecture in Python](https://www.youtube.com/watch?v=C7MRkqP5NRI)
* [A detailed summary of the Clean Architecture book by Uncle Bob](https://github.com/serodriguez68/clean-architecture)

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.