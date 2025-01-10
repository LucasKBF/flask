import sys
import os
from app import app


if __name__=="main":
    port = int(os.getenv("PORT"), "5000")
    app.run(host="0.0.0.0", port = port, debug=True)

