Collaboration Guidelines
==================================

1. Follow Git best practices:
   - Use feature branches for development.
   - Open pull requests for code reviews.
2. Write clean, modular, and well-documented code.
3. Use the `tests` folder to write unit and integration tests.

6S Collaboration Checklist
--------------------------

- **Site**
    - Ensure the code is in the correct place architecturally. Verify that new code fits within the intended module or class structure.
    - Keep dependencies explicit and use service objects, form objects, or helpers where appropriate.
    - Ensure proper integration with tools like Docker or CI pipelines.

- **Solid**
    - Follow SOLID principles:
        - **Single Responsibility:** Each class or function should do one thing well.
        - **Open/Closed Principle:** Classes should be open for extension but closed for modification.
        - **Liskov Substitution Principle:** Subtypes should be substitutable for their base types.
        - **Interface Segregation:** Prefer small, specific interfaces over general ones.
        - **Dependency Inversion:** Rely on abstractions, not concrete implementations.

- **SOFA**
    - Ensure methods are:
        - **Short:** Each method should focus on one task.
        - **One thing:** Maintain single-level abstraction within a function.
        - **Few arguments:** Minimize the number of arguments passed to functions.
        - **Abstraction:** Keep the level of abstraction consistent within a class or module.

- **Smells**
    - Avoid code smells such as:
        - **Deeply nested conditionals:** Refactor to improve readability.
        - **Redundant code:** Use DRY principles to eliminate repetition.
        - **Ambiguous naming:** Use descriptive, meaningful names for variables and methods.
        - **High complexity:** Simplify by breaking functions into smaller components.

- **Style**
    - Follow established coding standards for indentation, spacing, and naming conventions.
    - Use linters and formatters to enforce consistent style throughout the codebase.

- **Sign-off**
    - Perform thorough code reviews before merging into the main branch.
    - Test all changes using automated and manual tests.
    - Obtain team approval with comments like "LGTM" (Looks Good To Me) or equivalent.