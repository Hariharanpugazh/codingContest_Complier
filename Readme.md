
# Online Coding Contest Platform

This project allows users to create and participate in online coding contests.

## Requirements

- **Python 3.9**
- **Docker Desktop**
- **MongoDB Compass**

## Setting Up and Running the Project

### 1. Build and Run the Docker Container
1. Open the terminal in the root directory.
2. Run the following commands to build and run the Docker container:

   ```bash
   docker build -t my_compiler_container .
   docker run -d --name test_container my_compiler_container
   ```

---

### 2. Backend Setup

#### Activate the Virtual Environment
1. Navigate to the `backend` directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv envname
   envname\Scripts\activate
   ```

#### Install Dependencies
1. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

#### Run the Backend Server
1. Make database migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Start the backend server:

   ```bash
   python manage.py runserver
   ```

---

### 3. Frontend Setup

1. Navigate to the `frontend` directory.
2. Install the required npm packages:

   ```bash
   npm install
   ```

3. Start the frontend server:

   ```bash
   npm start
   ```

---

## Additional Notes

- Ensure that Docker Desktop is running before building and running the container.
- Use MongoDB Compass for managing the database.
- Make sure all dependencies are installed in their respective environments.

Enjoy hosting and participating in coding contests! 🎉
```
