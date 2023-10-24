# Library Management Flask Web Application with SQLAlchemy

## SUMMARY
This readme provides an overview of a Flask web application that utilizes SQLAlchemy to manage books, users, and loans. Currently, the application allows you to list all books, users and loans, but it is a work in progress and lacks the ability to display, add, edit, or delete individual items through an html-based webpage, but can be done through Thunder Client with a request.json file in VSCode or any similar tool.

## How to Install and Run the Project from GitHub

1. **Clone the Project Repository:**

   Open your terminal or command prompt and navigate to the directory where you want to store the project. Then, use the `git clone` command to clone the project repository from GitHub. Here's the command:

   ```bash
   git clone https://github.com/TotalWreck/Lib_proj.git
   ```

2. **Navigate to the Project Directory:**

   Change your current directory to the newly cloned project directory:

   ```bash
   cd Lib_proj
   ```

3. **Create a Virtual Environment (Optional but Recommended):**

   While not mandatory, it's a good practice to create a virtual environment to isolate your project's dependencies. This ensures that your project doesn't interfere with other Python installations on your system.

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Project Dependencies:**

   With your virtual environment activated, you can install the project's dependencies from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the necessary packages for your project.

5. **Run the Application:**

   You can now run the Flask application using the following command:

   ```bash
   python app.py
   ```

   The application will start, and you can access it in your web browser at `http://127.0.0.1:5000/`.

By following these steps, you'll successfully install and run the project from the GitHub repository on your local machine.

## IMPLEMENTED

## NOT IMPLEMENTED
