class ResultTextWriter:

    def __init__(self, file_name=None):
        self._file_name = file_name

    def write_content(self, content):
        if self._file_name:
            with open(self._file_name, "w") as text_file:
                text_file.write(content)
