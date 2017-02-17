# RestaurantMenu
This is the code for the final project from Udacity Full Stack Foundations Course.  The task was to create a CRUD menu app using Python, Flask, SQLite, SQLAlchemy and incorporting any type of styling (CSS, JS) required.  Rather than using standard forms this uses the WTForms extension for Flask.  It doesn't use any other front end frameworks for the UI.
This isn't production code as it lacks error handling and is only connected to the SQLite db.  The suggested course environment was Vagrant however I developed this using virtualenv (https://virtualenv.pypa.io/en/latest/index.html) and PyCharm.  Virtualenv can be used to create completely separate environments that don't share libraries with other installations or the global packages.  

This code needs the following dependencies.

Dependencies for the project:

Flask	0.12;
Jinja2	2.9.4;
MarkupSafe	0.23;
SQLAlchemy	1.1.4;
WTForms	2.1;
Werkzeug	0.11.15;
itsdangerous	0.24

In order to install create a virtualenv.  Activate the env, for example on windows: > \path\to\env\Scripts\activate.  Then install the dependencies (dependencies.txt) using pip "pip install -r dependencies.txt". Start the server on port 5000 for finalProject.py then navigate to localhost:5000 to see the app.

