### config.py

import sys
from PySide6.QtGui import QFont

# print(sys.platform)
# print(sys.version)
# print(sys.version_info)


def getFont():
    if sys.platform == 'darwin':  # mac
        font = QFont('Monaco', 12)
    elif sys.platform.find('linux') != -1:
        font = QFont('Monospace', 10)
    else:
        font = QFont('Courier New', 10)
    return font