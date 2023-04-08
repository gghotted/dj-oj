from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.fields.files import FileDescriptor
from private_storage.fields import PrivateFileField


class TemporaryUnZip:

    def __init__(self, zip_file_path, work_dir=None):
        self.zip_file_path = zip_file_path
        self.work_dir = work_dir

    def __enter__(self):
        self.dir = TemporaryDirectory(dir=self.work_dir)
        zip_file = ZipFile(self.zip_file_path, 'r')
        zip_file.extractall(self.dir.name)
        return Path(self.dir.name)

    def __exit__(self, exc, value, tb):
        self.dir.cleanup()


class TemporaryZipFileDescriptor(FileDescriptor):

    def __get__(self, instance, cls=None):
        file = super().__get__(instance, cls)
        file.unzip = partial(TemporaryUnZip, file.path, work_dir=self.field.work_dir)
        return file


class TemporaryZipFileField(PrivateFileField):
    descriptor_class = TemporaryZipFileDescriptor

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [FileExtensionValidator(['zip'])])
        self.work_dir = kwargs.pop('work_dir', None)
        super().__init__(*args, **kwargs)
