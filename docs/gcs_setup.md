

# Preparing to deploy Flask App via Google Cloud Platform (GCP)  
**GCP Project Setup**
1.  Login to [GCP Console](https://console.cloud.google.com/)
1.  Create New Project and record ID
**GCP PostgreSQL Generation**
1.  Create GCP PostgreSQL Instance in that Project:  Menu > SQL > Create Instance > Choose PostgreSQL
    *  Choose sandbox to obtain cheapest option
1.  After instance created:
    *  Create user (default is 'postgres') and password (password should not contain '@')
    *  Create database called `production`
    *  Go to site like https://whatismyipaddress.com/ to find your IP Address
    *  In Connections section, add to the Networking tab your computers IP address as a 'New Network'
1.  Using pgAdmin 4 v6+, create connection:
    *  Create sever (name is arbitrary)
    *  Add connection info:  GCP DB IP address, password, port.
1.  Create schema using SQL files in pgAdmin query tool
    *  Use key.sql file to generate schema
    *  Use triggers.sql to add pgSQL automated logic
    *  Use data.sql file to add data
1.  If testing program, change the ENV variable in the query.py and setup.py files.  
**Setup GCP CLI**
1.  Install the [gcloud CLI](https://cloud.google.com/sdk/docs/install)
1.  The base components of gcloud CLI has changed in the past.  The current status can be found [online](https://cloud.google.com/sdk/docs/components).  If a component for using the app engine is not default then the CLI will ask permission to install the needed components.  
1.  During the first time using the shell, you will need to login via your google account when requested.
1.  Select the project that you created previously
1.  The terminal will look like it is running from your local machine.  In that command line enter the following command to ensure App Engine Extensions are available `gcloud components install app-engine-python`
1.  You may get new windows popping up asking you to approve installations.
**Create GCP Engine Config Files**
1.  Create a requirements file in the root directory via terminal:
    * Activate environment: `. venv/Scripts/activate`
    * Run from the root directory: `pip freeze > requiremnts.txt`  
1.  Create [configuration file](https://cloud.google.com/appengine/docs/legacy/standard/python/config/appref) in the root directory:
    *  Name file `app.yaml`
    *  Contents:  
        ```
        runtime: python
        env: flex
        entrypoint: gunicorn -b :$PORT app:app
        ```  
**Deployment**
1.  Run in CLI:  `gcloud auth login gcloud config set project [YOUR_PROJECT_ID]`
1.  Initialize app engine:  `gcloud app create --project=MY-PROJECT-ID`
1.  Deploy app:  `gcloud app deploy`