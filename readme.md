
# Django Backend with User Authentication and Admin Roles

This project is a Django backend setup with PostgreSQL for user authentication, including admin roles. It provides endpoints for user registration, login, profile management, and admin user management.

## Prerequisites

- Python 3.x
- PostgreSQL
- Virtualenv
- Thunder Client (VS Code extension) or any other API testing tool

## Setup Instructions

### Step 1: Clone the Repository

\`\`\`bash
git clone <repository_url>
cd <repository_name>
\`\`\`

### Step 2: Create and Activate Virtual Environment

\`\`\`bash
python -m venv myenv
\`\`\`

For Windows:
\`\`\`bash
myenv\Scripts\activate
\`\`\`

For macOS/Linux:
\`\`\`bash
source myenv/bin/activate
\`\`\`

### Step 3: Install Dependencies

\`\`\`bash
pip install django psycopg2-binary djangorestframework djangorestframework-simplejwt
\`\`\`

### Step 4: Setup PostgreSQL

1. **Install PostgreSQL**: Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/).

2. **Create a Database and User**:
   - Open pgAdmin and create a new database (e.g., `myprojectdb`).
   - Create a new user (e.g., `myprojectuser`) and set a password.
   - Grant all privileges to the user for the database.

3. **Configure Database in Django**: Update `DATABASES` in `myproject/settings.py`:
   \`\`\`python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'myprojectdb',
           'USER': 'myprojectuser',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   \`\`\`

### Step 5: Apply Migrations

\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### Step 6: Create a Superuser

\`\`\`bash
python manage.py createsuperuser
\`\`\`

### Step 7: Run the Development Server

\`\`\`bash
python manage.py runserver
\`\`\`

## Endpoints

### 1. Register

- **URL**: `http://127.0.0.1:8000/api/register/`
- **Method**: `POST`
- **Body**:
  \`\`\`json
  {
      "email": "user@example.com",
      "name": "User",
      "phone_number": "1234567890",
      "employee_id": "EMP001",
      "profile_pic": null,
      "password": "password"
  }
  \`\`\`

### 2. Obtain JWT Token

- **URL**: `http://127.0.0.1:8000/api/token/`
- **Method**: `POST`
- **Body**:
  \`\`\`json
  {
      "email": "user@example.com",
      "password": "password"
  }
  \`\`\`
- **Response**:
  \`\`\`json
  {
      "refresh": "your_refresh_token",
      "access": "your_access_token"
  }
  \`\`\`

### 3. Access Profile

- **URL**: `http://127.0.0.1:8000/api/profile/`
- **Method**: `GET`
- **Headers**:
  \`\`\`plaintext
  Authorization: Bearer your_access_token
  \`\`\`

### 4. Admin View All Users

- **URL**: `http://127.0.0.1:8000/api/admin/users/`
- **Method**: `GET`
- **Headers**:
  \`\`\`plaintext
  Authorization: Bearer your_access_token
  \`\`\`

### 5. Admin Update or Delete User

- **URL**: `http://127.0.0.1:8000/api/admin/users/<user_id>/`
- **Method**: `PUT` or `DELETE`
- **Headers**:
  \`\`\`plaintext
  Authorization: Bearer your_access_token
  \`\`\`
- **Body (for PUT)**:
  \`\`\`json
  {
      "email": "user@example.com",
      "name": "Updated User",
      "phone_number": "0987654321",
      "employee_id": "EMP002",
      "profile_pic": null
  }
  \`\`\`

## Testing with Thunder Client

1. **Install Thunder Client**: Install the Thunder Client extension from the VS Code Extensions Marketplace.

2. **Obtain Token**:
   - Create a new request with the following details:
     - **Method**: `POST`
     - **URL**: `http://127.0.0.1:8000/api/token/`
     - **Body**:
       \`\`\`json
       {
           "email": "user@example.com",
           "password": "password"
       }
       \`\`\`
   - Send the request and copy the `access` token from the response.

3. **Access Profile**:
   - Create a new request with the following details:
     - **Method**: `GET`
     - **URL**: `http://127.0.0.1:8000/api/profile/`
     - **Headers**:
       \`\`\`plaintext
       Authorization: Bearer your_access_token
       \`\`\`
   - Send the request to access the profile data.

By following these steps, you can set up, run, and test your Django backend with user authentication and admin roles. If you encounter any issues, please refer to the Django documentation or seek further assistance.
