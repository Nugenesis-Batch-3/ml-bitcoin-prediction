"""
Launch HTTP server
"""

from app import app

DEV_MODE = False


if __name__ == "__main__":

    BIND_IP = "127.0.0.1" if DEV_MODE else "0.0.0.0"

    app.run(host=BIND_IP, debug=DEV_MODE)
