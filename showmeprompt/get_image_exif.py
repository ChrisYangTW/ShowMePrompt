from pathlib import Path

from PIL import Image
import piexif
from piexif import helper


class ImageInformation:
    def __init__(self, file_path: Path):
        self._height = None
        self._width = None
        self._info = {}
        self._filename = ''
        self._positive = ''
        self._negative = ''
        self._settings = ''
        self._raw = ''
        self._raw_without_settings = ''
        self._filename = file_path.name
        self.load_image(file_path)

    def load_image(self, file_path):
        with Image.open(file_path) as im:
            self._width, self._height = im.size
            self._info = im.info
            if 'parameters' in self._info and im.format == 'PNG':
                self.handle_sd_png()
            elif 'exif' in self._info and im.format in ['JPEG', 'WEBP']:
                self.handle_sd_jpg_or_webp()
            # no NovelAI's image to test
            # elif self._info.get('Software') == 'NovelAI':
            #     self.handle_nai()

    def raw_format(self) -> None:
        """
        To format the self._raw (string data).
        :return:
        """
        if self._raw:
            positive_index_end = self._raw.find('\nNegative prompt:')
            negative_index_end = self._raw.find('\nSteps:')
            if positive_index_end < 0 or negative_index_end < 0:
                print('Prompt incomplete..')
            else:
                self._raw_without_settings = self._raw[:negative_index_end]
                self._positive = self._raw[:positive_index_end]
                self._negative = self._raw[positive_index_end + 19:negative_index_end]
                self._settings = self._raw[negative_index_end + 1:]

    def handle_sd_png(self):
        self._raw = self._info.get('parameters')
        self.raw_format()

    def handle_sd_jpg_or_webp(self):
        try:
            # to obtain exif data as a dictionary({“0th”:dict, “Exif”:dict,...})
            exif_dict = piexif.load(self._info.get('exif'))
            # to obtain UserComment info at exif_dict['Exif'][37519],
            # then convert value in exif format to str
            self._raw = piexif.helper.UserComment.load(exif_dict['Exif'][piexif.ExifIFD.UserComment])
        except KeyError as e:
            print('This image does not contain [UserComment] content.')
        except ValueError as e:
            print(e)
        else:
            self.raw_format()

    # todo: novelai image
    # def handle_nai(self):
    #     pass

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def positive(self) -> str:
        if not self._positive and not self._negative and not self._settings:
            return '*** No Prompt information ***'
        return self._positive

    @property
    def negative(self) -> str:
        return self._negative

    @property
    def settings(self) -> str:
        return self._settings

    @property
    def raw_without_settings(self) -> str:
        return self._raw_without_settings

    @property
    def raw(self) -> str:
        return self._raw


if __name__ == '__main__':
    for path in [
        # '1.png',
        # '2(loss).png',
        # '3(encode).jpg',
        # '4(real).jpg',
        # '5.png'
    ]:
        path = Path(f'example/{path}')
        img = ImageInformation(path)
        print(img.raw)
        print()
        print(img.raw_without_settings)
        print('-' * 10)
