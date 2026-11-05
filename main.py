import uvicorn
#import subprocess
#import sys
    
def iniciar_api():

    uvicorn.run("backend.api1:fa.app", host="localhost", port=5000, reload=True)

def iniciar_servidores():

    # self.iniciar_streamlit()
    iniciar_api()

if __name__ == "__main__":
    iniciar_servidores()
