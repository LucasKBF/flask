import sys
import os
from app import app



if __name__ == "__main__":
    # Define a porta, usando 5000 como padrão se não estiver definida
    port = int(os.getenv("PORT", 5000))  # Note que o padrão é 5000 como número, não string
    app.run(host="0.0.0.0", port=port, debug=True)

