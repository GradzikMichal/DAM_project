import json
from pathlib import Path

from PIL.ImageFile import ImageFile
from django.conf import settings


class ImageClass():
    def __init__(
            self,
            image_name: str,
            image_path: str,
            image_id: int | None | str = None,
            image_type: str = "png",
            image_file: ImageFile | None = None,
            folder_path: str | Path = settings.MEDIA_ROOT + '\\',
            user_id: str | int = "0",
            saved_file: bool = False
    ):
        self.image_name = image_name
        self.image_path = image_path
        self.image_id = image_id
        self.image_type = image_type
        self.image_file = image_file
        self.folder_path = folder_path
        self.user_id = user_id
        self.saved_file = saved_file

    def to_dict(self):
        object_dict = self.__dict__.copy()
        object_dict.pop('image_file')
        return object_dict

    def toRecognizeJSON(self):
        return {
            "image_id": str(self.image_id),
            "image_file": self.image_file.tobytes(),
        }


    def toDbJSON(self):
        return json.dumps(
            {
                "image_name": self.image_name,
                "folder_path": self.folder_path,
                "user_id": str(self.user_id),
            }
        ).encode('UTF-8')

    def saveImage(self):
        self.image_file.save(settings.MEDIA_ROOT + '\\' + str(self.image_id) + "." + self.image_type)
