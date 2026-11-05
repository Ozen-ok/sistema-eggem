import sys
import subprocess
from pathlib import Path

# Localiza a pasta onde está este script
BASE_DIR = Path(__file__).resolve().parent

# Monta o caminho do arquivo principal do Streamlit
APP_PATH = BASE_DIR / "frontend" / "st_app.py"

# Verifica se o arquivo existe
if not APP_PATH.exists():
    raise FileNotFoundError(
        f"Arquivo principal não encontrado: {APP_PATH}"
    )

# Inicia o Streamlit
subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APP_PATH),
        "--server.port",
        "5001",
    ],
    check=True,
)