# librarysite

Library API.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Description

This project is a library API.

## Installation

To install and run the library API, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://gitlab.com/Selector0073/librarysite
    cd librarysite
    ```

2.  **Set up the environment variables:**

    *   Create .env file using the .env.example template.

3.  **Start the container:**

    ```bash
    docker compose up
    ```

4.  **Acces the API:**

    The API should now be accessible at `http://localhost:8000`.
    The mail client should now be accessible at `http://localhost:8025`.

## Usage

*   **Access the API:** Make an http request through a program like Postman.
*   **Admin interface:** Access the admin interface by navigating to `http://localhost:8000/admin/`. Log in with the superuser credentials (default: username:`admin` password:`adminpass`).
*   **Acces the mail client:** emails can be read in MailHog at `http://localhost:8025`.

## License

This project is licensed under the MIT License.