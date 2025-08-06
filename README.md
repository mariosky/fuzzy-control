# Install

## Get Docker

From <a href="https://docs.docker.com/get-started/get-docker/" target="_blank">here</a>

## Create a Python environment
```
python3 -m venv venv
pip3 install -r requirements.txt
```


## If using Windows PowerShell
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

## Docker compose
docker-compose up --scale worker=7 --remove-orphans

## Rebuild Workers 
docker-compose up --rebuild -d 

## Run the algorithms
1. Change the configuration file (`config.json`) 
2. Run the workers using `docker compose`
3. Run the controller in another terminal with `pyhton distributed.py`
