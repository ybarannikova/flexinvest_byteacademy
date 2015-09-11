# Flex Invest
#### Web Platform for Restructuring and Selling Assets

This prototype, built through the Django framework on top of PostgreSQL,
restructures fixed-rate assets and provides a GUI for purchasing the
residual tranches.

The application includes a custom administration portal primarily for
managing user access and permissions.

Further functionality coming soon:
- Portfolio management
- Reporting & analysis

## Technical Features, Languages & Libraries

#### Features
- Password encryption
- User sessions 
- User permissions
- Quandl API
- Manage.py commands
- Mobile & Desktop optimized GUI

#### Languages
- Python
- HTML
- CSS
- JavaScript

#### Libraries
- JQuery
- Requests
- Django Auth, Timezone

## Setup

     $ virtualenv venv
     $ source venv/bin/activate
     $ pip3 install -r requirements.txt
     
     $ python3 manage.py makemigrations
     $ python3 manage.py migrate
     $ python3 manage.py setupgroups
     $ python3 manage.py createsuperuser
     $ username: admin
     $ password: password
     
     $ python3 manage.py seed [flex_investor_user] [flex_analyst_user] [scenario1] [scenario2]
     # seed alone will run all options by default


     
     
