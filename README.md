# BlckLap

![Python](https://img.shields.io/badge/Python-14354C.svg?logo=python&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-1572B6.svg?logo=css3&logoColor=white) ![HTML](https://img.shields.io/badge/HTML-E34F26.svg?logo=html5&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-07405e.svg?logo=sqlite&logoColor=white) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?logo=visual-studio-code&logoColor=white)

[![Author](https://img.shields.io/badge/Author-PyDevyn-orange)](https://github.com/surbd)

Blcklap is an Authentication project built with Flask. It comprises of basic login and actions and account management options.

## Features

- Registration, Login and Logout
- Protected Routes
- Account Verification
- Account Management (Profile update)
- Password Reset (Forgot Password)



## Installation

You would find required dependencies to run BlckLap on your local machine in the `requirements.txt` file.

Clone this Repo
```sh
git clone git@github.com:SurbD/BlckLap.git
```
Create a virtual environment and activate it (use `source venv\bin\activate` for mac)
```sh
python -m venv venv-name
venv\Scripts\activate
```
> Make sure you create the virtual environment is the project directory

Install the dependencies and start the server.

```sh
pip install -r requirements.txt
FLASK_APP=run.py
```
```
python run.py
```
> Environments variables like `BLCKLAP_SECRET_KEY`, `EMAIL_USER`
> and `EMAIL_PASS` others would have to be manually set

## BlckLap User Interface

##### Landing Page
![BlckLap Landing Page](flaskapp/static/images/blcklap-landing-page.png)
##### Register Page
![BlckLap Register Page](flaskapp/static/images/blcklap-register.png)
##### Login Page
![BlckLap Login Page](flaskapp/static/images/blcklap-login.png)
##### Change Password
![BlckLap Change Password Page](flaskapp/static/images/blcklap-change-password.png)