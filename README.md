# Install
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
1. Change the configuration file
2. Run the workers using docket-compose
3. Run in another terminal the controller ~pyhton distributed.py~
