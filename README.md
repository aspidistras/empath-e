### **Empath-e** is a project designed to fight against psychophobia by developping empathy online. It allows users who want to raise awareness and inform on a mental disorder to get in contact with users who want to understand and know more about it.

Visit the website : https://empath-e.fr


# HOW TO USE LOCALLY

1. Clone the repository
2. Set up your virtual environment
3. Install dependencies by running : 
    ```
    pip install -r requirements.txt
    ```

4. Set up your PostgreSQL database :
    ```
    >> CREATE USER your_name WITH PASSWORD 'your_password';
    >> CREATE DATABASE empath_e;
    >> GRANT ALL ON DATABASE empath_e TO 'your_name';
    ```

5. Set up your TwiML app to enable browser calling : 

6. Create a .env file and append the following environment variables to it like this :

    - ADMIN_EMAIL=your_admin_email
    - MY_PASSWORD=your_email_password (to be generated in your account settings)
    - TWILIO_ACCOUNT_SID=your_twilio_account_sid
    - TWILIO_AUTH_TOKEN=your_twilio_auth_token
    - TWIML_APPLICATION_SID=your_twiml_app_sid

7. Run the following command in order to launch a redis server for the chat :
    ```
    docker run -p 6379:6379 -d redis:5
    ```

8. Use Ngrok to be able to make browser calls (service needs a public url to work with that you need to add to your Twiml app as : http://your-ngrok-url/contact/call/ ) :  

    - https://dashboard.ngrok.com/get-started/setup
    - 
        ```
        ./ngrok http 8000 
        ```

9. To gather ressources data :

    - 
        ```
        python manage.py shell
        ```
    - 
        ```
        >>> from app.data import disorders_batch
        >>> disorders_batch.get_disorders_data()
        ```

10. Run the development server : 
    ```
    python manage.py runserver
    ```








# SOURCES

BOOTSTRAP TEMPLATE :
https://startbootstrap.com/themes/creative/


CODE :
- https://docs.djangoproject.com/en/2.2/
- https://stackoverflow.com
- https://djangobook.com
- http://sametmax.com
- https://channels.readthedocs.io/en/latest/
- https://learndjango.com
- https://django-filter.readthedocs.io/en/stable/ref/filters.html
- https://www.twilio.com/docs/voice/tutorials/browser-calls-python-django
- https://github.com/TwilioDevEd/browser-calls-django
- https://dashboard.ngrok.com/get-started/setup


RESOURCES : 
- https://www.passeportsante.net
- http://www.bipoles31.fr/
- https://www.fondation-fondamental.org
- https://fr.wikipedia.org/
- http://www.prendresoin.org/wp-content/uploads/2014/02/La-personnalite-antisociale.pdf