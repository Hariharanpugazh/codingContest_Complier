# Online Coding Contest Compiler

This project replicates the functionality of the Coding Contest page of the Unstop website. It allows users to create coding challenges, attempt coding problems, and evaluate their solutions in multiple programming languages like Python, Java, C, and C++. The project is developed using a **React-based frontend** and a **Python Django backend**, with a compiler setup to handle code execution in multiple languages.

---

## Features

- **Create Contests**: Admin users can create new coding contests, set problems, and define scoring.
- **Trigger Test**: Users can trigger their code for evaluation against sample test cases.
- **Support for Multiple Languages**: Python, Java, C, and C++ are supported for coding challenges.
- **Integrated Compiler**: Code execution and evaluation handled by a backend compiler.
- **Real-time Results**: Users get real-time feedback on the correctness and performance of their solutions.

---

## Requirements

### Frontend
- Node.js (v14 or higher)
- npm or yarn (for managing dependencies)

### Backend
- Python (3.10 or higher)
- Django (latest stable version)
- Docker (for setting up the compiler environment)
- PostgreSQL (for database setup)

### Compiler Setup
- Docker images for compiling C, C++, Python, and Java code.

---

## Installation Guide

### Clone the Repository

```bash
git clone https://github.com/Hariharanpugazh/codingContest_Complier.git
cd codingContest_Complier
```

---

### Frontend Setup

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

   The frontend should now be running on `http://localhost:3000`.

---

### Backend Setup

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

5. Set up the database connection:
   - Install PostgreSQL and create a new database named `coding_contest`.
   - Update the `settings.py` file with your PostgreSQL credentials.

6. Run database migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Start the Django server:

   ```bash
   python manage.py runserver
   ```

   The backend should now be running on `http://127.0.0.1:8000`.

---

### Compiler Setup with Docker

1. Make sure Docker is installed and running on your system.

2. Pull Docker images for the required languages (Python, Java, C, C++):

   ```bash
   docker pull madhanp7/multi-language-compiler-updated
   ```

3. Ensure that Docker can be accessed from the backend code to compile and execute user submissions.

---

### Running the Project

1. Make sure the backend server, frontend server, and Docker are running.
2. Open the frontend in your browser (`http://localhost:3000`).
3. As an admin, create new contests and coding problems.
4. Users can register, participate in contests, submit solutions, and receive real-time results.

---

## Commands Cheat Sheet

### Frontend

- Install dependencies: `npm install`
- Start development server: `npm start`
- Build for production: `npm run build`

### Backend

- Create virtual environment: `python -m venv venv`
- Activate virtual environment:
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`
- Start server: `python manage.py runserver`

### Docker

- Pull Docker image: `docker pull madhanp7/multi-language-compiler-updated`
- List running containers: `docker ps`
- Start/Stop containers as required.

---

## File Structure

```
codingContest_Complier
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   └── App.js
│   └── package.json
│
├── backend/
│   ├── coding_contest/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
│
└── README.md
```

---

## Notes

- Ensure Docker is properly set up and accessible to run the compiler.
- For beginners:
  - Refer to [Django Documentation](https://docs.djangoproject.com/en/stable/) for understanding backend development.
  - Explore React tutorials at [React Docs](https://react.dev/learn) for frontend understanding.
  - Learn more about Docker from [Docker Documentation](https://docs.docker.com/get-started/).

---

Feel free to contribute to the project by creating issues or submitting pull requests!

---

