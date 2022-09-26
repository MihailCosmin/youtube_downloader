import PySide6


class BrowseDirectory(PySide6.QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFileMode(PySide6.QtWidgets.QFileDialog.Directory)

    def get_path(self):
        return self.getExistingDirectory(self.parent, "Select Directory")