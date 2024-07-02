# Car Rental System

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a MySQL database and update the `DATABASES` setting in `car_rental_system/settings.py`.
5. Apply the database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
7. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Endpoints

- `/api/signup/` - Register a new user.
- `/api/login/` - Login a user.
- `/api/car/create/` - Add a new car (Admin only).
- `/api/car/get-rides/` - Get available rides.
- `/api/car/rent/` - Rent a car.
- `/api/car/update-rent-history/` - Update rent history (Admin only).
