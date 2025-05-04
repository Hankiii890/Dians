import sys
import os
import threading
import uvicorn
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def run_server():
    try:
        from api.routers import app as routes_app
    except ImportError as e:
        print(f"Failed to import api.routes: {e}")
        return

    app = routes_app
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Start the FastAPI server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Start the PyQt5 GUI
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())