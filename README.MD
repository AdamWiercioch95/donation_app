
# Donate to Charity Project

Welcome to the Donate to Charity project! This web app is designed to help users donate items such as toys, clothes, rugs, food, utilities, and home goods to foundations, NGOs, or local charities. It also allows users to schedule a courier for convenient pickup of donated items.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Visualization](#visualization)
- [License](#license)
- [Author](#author)

## Description

This project was developed as part of a Python and frontend course. The app offers a full CRUD (Create, Read, Update, Delete) functionality and was created using the Django framework, covering both backend and frontend development.

## Features

- **Backend Development**: Implemented models, views, and database setup.
- **Template Integration**: Created new templates and integrated existing scaffold templates.
- **Styling**: Designed user profile pages.
- **JavaScript Implementation**: Added features form validation.
- **Testing**: Comprehensive tests to ensure functionality and reliability.

## Technologies

- **Framework**: Django
- **Languages**: Python, JavaScript, CSS, HTML
- **Database**: PostgreSQL
- **Others**: pytest, pytest-django, venv

## Installation

To get started with the project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/donate-to-charity.git
   cd donate-to-charity
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Configure environment files**:
- Navigate to env directory and create a `.env` file based on the `.env-default` file
   ```bash
    cp env/.env-default env/.env
    ```
- Edit the `env/.env` file to fit your environment (e.g., database settings, API keys, etc.).


4. **Set up the database**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

To use the application, open your web browser and go to \`http://127.0.0.1:8000\`. You can register as a new user, log in, and start donating items. The app allows you to manage your donations, view your donation history, and view your user settings.

## Testing
 ```bash
 pytest <app_name>/tests.py
 ```

## License

This project is licensed for private, personal use. You are free to use, modify, and distribute this application as you see fit.

## Author

Developed by [AdamWiercioch95](https://github.com/AdamWiercioch95)