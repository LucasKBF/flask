import sys
import os
from app import app
import ctypes
titulo = "SigaaV2"
ctypes.windll.kernel32.SetConsoleTitleW(titulo)


if __name__ == "__main__":
    # Define a porta usando 5000
    port = int(os.getenv("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=True)

