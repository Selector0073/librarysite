# librarysite

Library API.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Description

This project is a library API.

## Installation

To install and run the library API, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://gitlab.com/Selector0073/librarysite.git
    cd librarysite
    ```

2.  **Set up the environment:**

    *   Make sure you have Python installed (preferably version 3.12).
    *   It's recommended to use a virtual environment to manage dependencies.

        ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Linux/macOS
        venv\Scripts\activate  # On Windows
        ```

3.  **Install dependencies:**

    ```bash
    pip install -r Pipfile
    ```

4.  **Configure the database:**

    *   Set up a PostgreSQL database. You can use the provided `docker-compose.yaml` to run a local PostgreSQL instance using Docker.

        ```bash
        docker-compose up -d
        ```

    *   Update the `.env` file with your database credentials.  An example `.env` file is provided.

        ```
        SECRET_KEY=your-secret-key-here
        DEBUG=True

        DB_NAME=librarysite_db
        DB_USER=librarysite_user
        DB_PASSWORD=your-secure-password-here
        DB_HOST=localhost
        DB_PORT=5432

        EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
        EMAIL_HOST=localhost
        EMAIL_PORT=1025
        EMAIL_USE_TLS=False
        EMAIL_USE_SSL=False
        EMAIL_HOST_USER=
        EMAIL_HOST_PASSWORD=
        DEFAULT_FROM_EMAIL=test@example.com
        ```

5.  **Apply migrations:**

    ```bash
    python librarysite/manage.py migrate
    ```

6.  **Create a superuser:**

    ```bash
    python librarysite/manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python librarysite/manage.py runserver 0.0.0.0:8000
    ```

    The API should now be accessible at `http://localhost:8000`.

## Usage

*   **Access the API:** Make an http request through a program like Postman.
*   **Admin interface:** Access the admin interface by navigating to `http://localhost:8000/admin/`. Log in with the superuser credentials you created during installation.

## Contributing

Contributions are welcome! Here's how you can contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Test your changes thoroughly.
5.  Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.