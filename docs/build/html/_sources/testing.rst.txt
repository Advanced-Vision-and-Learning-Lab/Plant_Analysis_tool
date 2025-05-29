Testing
=======

Testing is a crucial part of the development process. It ensures that the code is working as expected and that it is free of bugs. 

Some important concepts about testing are:

- **Unit Testing:** Tests individual components of the code in isolation. It is used to ensure that each part of the code works correctly.
- **Integration Testing:** Tests how different components of the code work together. It is used to ensure that the code works as a whole.
- **Test Coverage:** Measures the percentage of code that is covered by tests. It is used to ensure that all parts of the code are tested.


Writing Tests
----------------

Since this app has many services and components, it is important to write tests for each part of the code. Each service should have its own set of tests to ensure that it works correctly.

Some important points to consider while writing tests are:

- **Test Isolation:** Tests should be independent of each other. They should not rely on the state of other tests.
- **Test Database:** Use a separate database for testing to avoid conflicts with the development database. This is reason for the test database in the docker-compose file.
- **Mocking:** Use mocking to simulate external dependencies like APIs or databases. This ensures that the tests are fast and reliable.
- **Test Coverage:** Aim for high test coverage to ensure that all parts of the code are tested.
- **Fixtures and Factories:** Use fixtures and factories to create test data. This makes it easier to write tests and ensures that the data is consistent.

Tests should be organized into different folders based on the service or component they are testing. For example, tests for the backend API should be in the `src/tests/api/backend` folder, and tests for the frontend API should be in the `src/tests/api/frontend` folder.



Running Tests
----------------

To run the tests for the plant phenotyping application, follow these steps:

1. Log in to the service container where the tests are located:

   .. code-block:: bash

       docker-compose exec <service-name> bin/bash

2. You can run tests for specific folder using:

   .. code-block:: bash

       ENVIRONMENT=test pytest <folder under test> --cov=<folder to include in the coverage report> --cov-report=term-missing --cov-report=html

   For example, to run tests for the frontend API:
    
   .. code-block:: bash

       ENVIRONMENT=test pytest src/tests/api/frontend --cov=src/api/frontend --cov-report=term-missing --cov-report=html

3. Alternatively, you can run all tests using:

   .. code-block:: bash

       ./run_tests.sh