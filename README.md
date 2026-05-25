# CodeAlpha Event Registration System

This project implements **Task 2** from the CodeAlpha backend internship assignment: an event registration system backend using **Django** and **SQLite**.

## Features

- List all events: `GET /api/events/`
- View event details: `GET /api/events/<id>/`
- Submit event registration: `POST /api/register/`
- View registrations: `GET /api/registrations/`
- Cancel a registration: `DELETE /api/registrations/<id>/`
- Admin panel for event and registration management: `GET /admin/`

## Setup

1. Open the project folder in your terminal.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Open the API at:
   ```
   http://127.0.0.1:8000/
   ```

## API Examples

### Get all events

```bash
curl http://127.0.0.1:8000/api/events/
```

### Get event details

```bash
curl http://127.0.0.1:8000/api/events/1/
```

### Register for an event

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Aman","last_name":"Kumar","email":"aman@example.com","phone":"9876543210","event_id":1}'
```

### View registrations by email

```bash
curl "http://127.0.0.1:8000/api/registrations/?userEmail=aman@example.com"
```

### Cancel a registration

```bash
curl -X DELETE http://127.0.0.1:8000/api/registrations/1/
```

## Notes

- The project uses `db.sqlite3` for the Django database.
- Django admin is enabled for event and registration management.
- The API is implemented using Django REST Framework.
