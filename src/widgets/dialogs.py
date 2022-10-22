from PySide6.QtWidgets import QFileDialog


class BrowseDirectory(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFileMode(QFileDialog.Directory)

    def get_path(self):
        return self.getExistingDirectory(self.parent, "Select Directory")