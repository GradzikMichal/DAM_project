import json

from django.conf import settings


class ImageClass():
    def __init__(
            self,
            image_name,
            image_file,
            image_id=None,
            folder_path=settings.MEDIA_ROOT + '\\',
            user_id="0",
            saved_file=False
    ):
        self.image_name = image_name
        self.image_file = image_file
        self.image_id = image_id
        self.folder_path = folder_path
        self.user_id = user_id
        self.saved_file = saved_file

    def to_dict(self):
        object_dict = self.__dict__.copy()
        object_dict.pop('image_file')
        return object_dict

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.to_dict(),
            sort_keys=True,
            indent=4
        ).encode('UTF-8')


