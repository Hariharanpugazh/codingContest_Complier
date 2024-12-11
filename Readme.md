
# Test-portal

A platform to manage coding contests with a backend to handle user submissions and a frontend for a seamless user experience. The project includes a Docker-based compiler for multiple languages such as Python, Java, C, and C++.

## Features
- User-friendly frontend interface built with React.
- Robust backend built using Django with PostgreSQL for database management.
- Multi-language compiler using Docker containers.

---

## Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/mk070/ihub-test-portal
cd ihub-test-portal
```

---

### 2. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The frontend should now be running on [http://localhost:3000](http://localhost:3000).

---

### 3. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```


5. Start the Django server:
   ```bash
   python manage.py runserver
   ```

   The backend should now be running on [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

### 4. Compiler Setup with Docker
1. Ensure Docker is installed and running on your system.

2. Build Docker images for the required languages (Python, Java, C, C++):

   - Build images using check your working directory for `Dockerfile`:
     ```bash
     docker build -t <image-name> .
     ```

3. Create and run a Docker container named `test_container`:
   ```bash
   docker run --name test_container <image-name>
   ```

4. Ensure the backend code has access to Docker for compiling and executing user submissions.

---
