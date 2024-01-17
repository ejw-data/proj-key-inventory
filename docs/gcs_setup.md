

# Preparing to deploy Flask App via Google Cloud Platform (GCP)  

1.  Login to [GCP Console](https://console.cloud.google.com/)
1.  Create New Project and record ID
1.  Create app.yaml in root directory
1.  Run in gitbash:  `gcloud auth login gcloud config set project [YOUR_PROJECT_ID]`
1.  Initialize app engine:  `gcloud app create --project=MY-PROJECT-ID`
1.  Deploy app:  `gcloud app deploy`