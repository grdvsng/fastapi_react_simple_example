#### Example of using FastAPI with Reac + create dev server wsl2 + docker
#### Setup
###### With vscode and docker
1. Download and install vscode https://code.visualstudio.com/  
2. Install wsl2 https://docs.microsoft.com/ru-ru/windows/wsl/install-manual
3. Install linux subsystem https://azuremarketplace.microsoft.com/en-us/marketplace/apps/credativ.debian?tab=overview
4. Download? install and configurate docker for using with wsl2 https://docs.docker.com/desktop/windows/wsl/
5. Configure wsl2 https://docs.microsoft.com/ru-ru/windows/wsl/tutorials/wsl-containers
6. Enjoy http://127.0.0.1:8000/

###### Usual
1. Walk to the rep directory
2. Run command 'pip install -r ./src/requirements'

* Run service command 'uvicorn src.main:app --host 0.0.0.0 --reload --port 8000'
* if server didn't start automaticly use command in terminal "uvicorn src.main:app --host 0.0.0.0 --reload"
* api docs http://127.0.0.1:8000/docs
* api interface http://localhost:8000/
* tests cmd "pytests"