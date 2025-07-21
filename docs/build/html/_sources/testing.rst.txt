Testing
=======

Testing is a crucial part of the development process. It ensures that the code is working as expected and that it is free of bugs.

Types of Tests
--------------
- **Unit Testing:** Test individual components in isolation.
- **Integration Testing:** Test how different components work together.
- **Test Coverage:** Measure the percentage of code covered by tests.

Writing Tests
-------------
- Write tests for each service (backend, frontend, worker).
- Use a separate test database to avoid conflicts with development data.
- Use mocking to simulate external dependencies (APIs, S3, etc.).
- Use fixtures and factories to create test data.
- Organize tests by service/component (e.g., `src/tests/api/backend`).

Running Tests
-------------
1. Log in to the service container where the tests are located:
   ```bash
   docker-compose exec <service-name> bash
   ```
2. Run tests for a specific folder:
   ```bash
   ENVIRONMENT=test pytest <folder> --cov=<folder> --cov-report=term-missing --cov-report=html
   ```
   Example for backend API:
   ```bash
   ENVIRONMENT=test pytest src/tests/api/backend --cov=src/api/backend --cov-report=term-missing --cov-report=html
   ```
3. Alternatively, run all tests using a script:
   ```bash
   ./run_tests.sh
   ```

Test Isolation and Coverage
---------------------------
- Tests should be independent and not rely on the state of other tests.
- Aim for high test coverage to ensure all code paths are tested.