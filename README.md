# Install
```
python3 -m venv venv
pip3 install -r requirements.txt
```


## En la terminal Windows PowerShell
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

## Docker compose
docker-compose up --scale worker=7 --remove-orphans

## Rebuild Workers 
docker-compose up --rebuild -d 


