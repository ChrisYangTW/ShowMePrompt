import re
from pathlib import Path

from PIL import Image
import piexif
from piexif import helper


class ImagePromptInfo:
    """
    Get the prompt information of an image
    """
    def __init__(self, file_path: Path):
        self._info = {}
        self._filename = ''
        self._positive = ''
        self._negative = ''
        self._settings = ''
        self._raw = ''
        self._raw_without_settings = ''
        self._filename = file_path.name
        self.parse_image(file_path)

    def parse_image(self, file_path: Path):
        with Image.open(file_path) as im:
            self._info = im.info
            if 'parameters' in self._info and im.format == 'PNG':
                self.handle_sd_png_image()
            elif 'exif' in self._info and im.format in ['JPEG', 'WEBP']:
                self.handle_sd_jpg_or_webp_image()
            elif self._info.get('Software') == 'NovelAI':
                print('\033[4m'  + 'NotImplemented: handle Nai image' + '\033[0m')

    def handle_sd_png_image(self):
        self._raw = self._info.get('parameters')
        self.raw_format()

    def handle_sd_jpg_or_webp_image(self):
        try:
            # to obtain exif data as a dictionary({“0th”:dict, “Exif”:dict,...})
            exif_dict = piexif.load(self._info.get('exif'))
            # to obtain UserComment info at exif_dict['Exif'][37519],
            # then convert value in exif format to str
            self._raw = piexif.helper.UserComment.load(exif_dict['Exif'][piexif.ExifIFD.UserComment])
        except KeyError as e:
            print('\033[33m' + f'KeyError: {e}, {self._filename} does not contain [UserComment] content.' + '\033[0m')
        except ValueError as e:
            print('\033[33m' + f'ValueError: {e} ({self._filename})' + '\033[0m')
        else:
            self.raw_format()

    def handle_nai_image(self):
        raise NotImplemented('Need to handle NovelAI\'s image')

    def raw_format(self) -> None:
        """
        To format the self._raw
        """
        if self._raw:
            positive_index_end = self._raw.find('\nNegative prompt:')

            # for civital.com Copy Generation Data structure(which setting info started with "Steps:")
            if match_string := re.search(r'(\nSteps:)|(\nSize:)', self._raw):
                negative_index_end = match_string.start()
            else:
                negative_index_end = -1

            if positive_index_end < 0 or negative_index_end < 0:
                print('\033[33m' + f'{self._filename} Prompt incomplete..' + '\033[0m')
            else:
                self._positive = self._raw[:positive_index_end]
                self._negative = self._raw[positive_index_end + 18:negative_index_end]
                self._settings = self._raw[negative_index_end + 1:]
                self._raw_without_settings = self._raw[:negative_index_end]

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def positive(self) -> str | None:
        if not self._positive and not self._negative and not self._settings:
            return None
        return self._positive

    @property
    def negative(self) -> str:
        return self._negative

    @property
    def settings(self) -> str:
        return self._settings

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def raw_without_settings(self) -> str:
        return self._raw_without_settings


if __name__ == '__main__':
    for path in [
        # '1.png',
        # '2(loss).png',
        # '3(encode).jpg',
        # '4(real).jpg',
        '5.png',
        'tt.jpeg'
    ]:
        print('<' * 10, path, '>' * 10)
        path = Path(f'../example/images/{path}')
        img = ImagePromptInfo(path)
        print(img.raw)
        print(img.positive)
        print(img.negative)
        print('_' * 80)
