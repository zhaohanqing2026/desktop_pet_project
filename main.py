import sys
from PySide6.QtWidgets import QApplication
from ui.pet_window import DesktopPet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet_window = DesktopPet()
    pet_window.show()
    sys.exit(app.exec())