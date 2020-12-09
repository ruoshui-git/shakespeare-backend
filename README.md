# Backend for Shakespeare GPT-2 model

After many many trials and failures, this is finally successfully deployed on Azure Web Services for Containers.

This repo is also hosted on [bitbucket](https://bitbucket.org/ruoshui-git/backend/src/main/) because bitbucket doesn't have Git LFS bandwidth quota.

# Running locally

## Using Docker (which I ended up using for deployment)

- Build: `docker build -t shakespeare-backend ./`
- Run: `docker run -d --name sp-container -p 9640:80 shakespeare-backend`

_Obviously, these are commands only for people who have never used Docker._

## Using good old plain normal pip

- Install requirements: `pip install -r requirements.txt`

It's very likely that GitHub will not clone "/model/pytorch_model.bin", which is stored in lfs. (I exceeded my bandwith quota already.)
BitBucket has no bandwith quota, but I didn't investigate how to clone with lfs. The size of the file is 487 MB, so if it's anything less than that on your disk, you don't have the right file.

If that's the case, run this in project root folder:

`pip install gdown && gdown https://drive.google.com/uc?id=1-8zTenijMztkEmkNJnpWppHaVx8uI6aC -O ./model/pytorch_model.bin`

- Run: `uvicorn main:app`

# Heroku failed for this one

I was trying to download the model with gdown, but it takes too long. Heroku will kill a worker if it doesn't respond within 30 sec. Downloading a ~500 MB model definite takes longer than that.

Also it seems like each worker is downloading their own copy of the model. Not good.
