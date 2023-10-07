---
layout: default
---
This document contains the basic GCP command I need in order to log in from my machine 

Copying files to the VM from the local machine
```bash
gcloud compute scp --project investigating-c-learning --zone us-west1-b --recurse <local file or directory> deeplearning-1-vm:~/
```
To login to the cloud
```bash
gcloud compute ssh --zone "us-west1-b" "deeplearning-1-vm" --project "investigating-c-learning"
```

Access jupyter notebook
```bash
gcloud compute instances describe --project investigating-c-learning --zone us-west1-b deeplearning-1-vm | grep googleusercontent.com | grep datalab
```
