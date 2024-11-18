# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

1. Why can we not easily split this project into two microservices?
   - Only one database is used. Each microservice should use its own database to maintain independence when dividing into Microservices.
   - The User use cases are directly accessing the Item repository. This is not an issue in a monolith, but it would become a problem if we were to split the database. In that case, the User microservice would need to make an API call to the Item microservice.
   - There are common modules (common.py, database.py, ...) that are used by both item and user.
2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?
   - User use cases are tightly coupled to the Item by directly using its repository.
   - The business logic layer (usecases.py) directly depends on the persistence layer (repository.py). Inner layers should not depend on outer layers. There is no intermediate interface being used to decouple them (Dependency Inversion Principle).
   - The database is being passed as a parameter to the use cases from the API. The repository interface dependency should be injected into the use cases instead of the database.
   - There are no business entities. Only DTOs (schemas) and database models exist, which depend on SQLAlchemy and, therefore, belong to the outer layer.
   - HTTPExceptions are being thrown from the use cases. These exceptions are from FastAPI, so the use cases depend on the framework, which is in the outermost layer (details). Generic exceptions should be thrown instead, which would be caught by the outer layer and re-thrown as HTTPExceptions from there.
   - DTO transformations are being done in the use cases. The use cases should only interact with domain entities (inner layer) since DTOs are used for external communication with the API. DTOs and their converters should only be visible to the outer layer, the framework (API).
   - The repository is not implementing an interface that allows the use cases to decouple.

3. What would be your plan to refactor the project to stick to the clean architecture?
   - Folders will be added within Item and User to better organize the layers. An organization that first divided by layers and then by entities could have been chosen, but I opted to leave the entities level first to make the single responsibility principle clearer.
   - Domain entities will be created to decouple from the database.
   - An interface will be created for repositories to implement and thus decouple the use cases from the outer layer. This will make it easier to create an in-memory repository without affecting the other layers.
   - DTOs and their converters will be moved to the external API layer (framework).
   - The repository interface will be injected into the use cases instead of the database directly.
   - The use cases will only interact with the domain entities.
   - Generic exceptions will be created to be thrown by the use cases by decouple them from the framework.

4. How can you make dependencies between modules more explicit?
   - I'll define the interface for the repositories. Use interfaces so that the use cases depend only on abstractions, not on concrete implementations.
   - I'll use dependency injection (both in the use cases and in the definition of the endpoints) to make the code more testable and decoupled.

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