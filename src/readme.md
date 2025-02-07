# SOLID Principles and Project Restructuring

The **SOLID Principle** contains a set of principles aimed at improving software design and maintainability.

The `payment_service` directory embodies various design patterns. 
This directory resulted from restructuring the `solid_principles` codebase found in the file `ater.py`.

## Identified Problem
The main issue with the original design is the presence of numerous lines of code within a single file, making it difficult to maintain.

## Restructuring the Project
To restructure the project:
1. Review all low-level classes and assign them categories based on their context and functionalities.
2. Create a folder for each context.
3. Create files where names reflect their respective functionalities.

### Separation Criteria:
- The main service or class that integrates the functionality of all modules should reside in the root directory.
- Classes with multiple constructors should go into a folder named `commons`. For each data type, there should be a separate file.
- Every directory needs an `__init__.py` file to enable access to its modules (e.g., `from directoryName import fileName`).
- Each protocol should have its own `.py` file.

## Characteristics:
- The directories `loggers` and `validators` do not depend on any protocol. On the other hand, `processors` and `notifiers` depend on protocols.
- The `processors` directory is particularly complex as it contains three protocols and three payment processors.

## Design Patterns  
Here're the design patterns with their uses at theirs respective files 

| Design Patterns         | Uses                                                                                   | Files                                                                                      |
|--------------------------|---------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **Strategy**             | Add the logic to choose the notification method between SMS and email.                | `service`, `notifier`, `email`, `sms`, `main`                                             |
| **Factory**              | Create a class for transaction processing (e.g., Stripe, Local, Offline) and assign it to `PaymentService`. | `commons:payment_data`, `factory`, `service`, `main`                                       |
| **Decorator**            | Enhance logs in the console to track the start and finish of transactions.            | `service_protocol`, `service`, `decorator_protocol`, `logging_service`, `main`            |
| **Builder**              | Simplify the creation of complex objects step by step.                                | `builder`, `factory`, `main`                                                              |
| **Observer**             | Notify accountability about the success or failure of a transaction.                  | `listener`, `manager`, `accountability_listener`, `service_protocol`                      |
| **Chain of Responsibility** | Create a chain of validations for customer and payment information during the payment process. | `commons:requests`, `ChainHandler`                                                        |

Thanks for read this, I hope this was usefull for you