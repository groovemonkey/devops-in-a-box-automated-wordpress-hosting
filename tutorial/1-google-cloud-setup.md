# 1. Google Cloud Setup

## Sign up for a GCP account

[Google Cloud Console](https://console.cloud.google.com)


## Install the Google Cloud SDK

[SDK Install](https://cloud.google.com/sdk/)

    tar zxvf $YOUR_TAR_GZ_FILE
    ./google-cloud-sdk/install.sh

Follow the prompts.


## Initialize the SDK

Start a new shell and then run:

    gcloud init

Open the generated link in your browser, log in with your Google Cloud account, and allow access.

In the shell, continue the initialization process.

- Select your existing (default) GCP project.
- Choose "Y" to configure Compute
- Choose a zone near you (e.g. 38). You'll see output like:

    Your project default Compute Engine zone has been set to [us-east1-d].
    You can change it by running [gcloud config set compute/zone NAME].

    Your project default Compute Engine region has been set to [us-east1].
    You can change it by running [gcloud config set compute/region NAME].


Congratulations, you have CLI access to your Google Cloud project!
