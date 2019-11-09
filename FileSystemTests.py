from fs.test import FSTestCases

from filesystem import DiscordFileSystem


class TestMyFS(FSTestCases):

    def make_fs(self):
        # Return an instance of your FS object here
        return DiscordFileSystem()

    def assert_exists(self, path):
        super().assert_exists(path)

    def assert_not_exists(self, path):
        super().assert_not_exists(path)

    def assert_isfile(self, path):
        super().assert_isfile(path)

    def assert_isdir(self, path):
        super().assert_isdir(path)

    def assert_text(self, path, contents):
        super().assert_text(path, contents)

    def assert_bytes(self, path, contents):
        super().assert_bytes(path, contents)
