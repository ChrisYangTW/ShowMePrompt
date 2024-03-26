import re
from pathlib import Path
from dataclasses import dataclass

from PIL import Image
import piexif
from piexif import helper


@dataclass(slots=True)
class ImagePromptsData:
    positive: str = ''
    negative: str = ''
    settings: str = ''
    raw: str = ''
    raw_without_settings: str = ''


class ImagePromptInfo:
    """
    Get the prompt information of an image
    """
    def __init__(self, file_path: Path) -> None:
        self._info: dict = {}
        self._positive: str = ''
        self._negative: str = ''
        self._settings: str = ''
        self._raw: str = ''
        self._raw_without_settings: str = ''
        self._file_path: Path = file_path
        self.parse_image(file_path)

    def parse_image(self, file_path: Path) -> None:
        with Image.open(file_path) as im:
            self._info = im.info
            if 'parameters' in self._info and im.format == 'PNG':
                self.handle_sd_png_image()
            elif 'exif' in self._info and im.format in ['JPEG', 'WEBP']:
                self.handle_sd_jpg_or_webp_image()
            elif 'XML:com.adobe.xmp' in self._info:
                self.handle_sd_image_make_by_draw_things()
            elif self._info.get('Software') == 'NovelAI':
                print('\033[4m' + 'NotImplemented: handle Nai image' + '\033[0m')

    def handle_sd_png_image(self) -> None:
        self._raw = self._info.get('parameters')
        self.raw_format()

    def handle_sd_jpg_or_webp_image(self) -> None:
        try:
            # to obtain exif data as a dictionary({“0th”:dict, “Exif”:dict,...})
            exif_dict = piexif.load(self._info.get('exif'))
            # to obtain UserComment info at exif_dict['Exif'][37519],
            # then convert value in exif format to str
            self._raw = piexif.helper.UserComment.load(exif_dict['Exif'][piexif.ExifIFD.UserComment])
        except KeyError as e:
            print('\033[33m' + f'KeyError: {e}, {self._file_path.name} does not contain [UserComment] content.' + '\033[0m')
        except ValueError as e:
            print('\033[33m' + f'ValueError: {e} ({self._file_path.name})' + '\033[0m')
        else:
            self.raw_format()

    def handle_sd_image_make_by_draw_things(self) -> None:
        xmp_data: str = self._info['XML:com.adobe.xmp']
        if '<xmp:CreatorTool>Draw Things</xmp:CreatorTool>' not in xmp_data:
            return

        prompts_info_start = xmp_data.find('<rdf:li xml:lang="x-default">')
        prompts_info_end = xmp_data.find('</rdf:li>')
        prompts_info = xmp_data[prompts_info_start+29:prompts_info_end]

        prompts_info = prompts_info.replace(r'&#xA;-', '\nNegative prompt: ', 1).replace(r'&#xA;', '\n', 1)
        self._raw = prompts_info
        self.raw_format()

    def handle_nai_image(self) -> None:
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
                print('\033[33m' + f'{self._file_path.name} Prompt incomplete..' + '\033[0m')
            else:
                self._positive = self._raw[:positive_index_end]
                self._negative = self._raw[positive_index_end + 18:negative_index_end]
                self._settings = self._raw[negative_index_end + 1:]
                self._raw_without_settings = self._raw[:negative_index_end]

    @property
    def filename(self) -> str:
        return self._file_path.name

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

    @property
    def prompts(self) -> ImagePromptsData:
        if not self._positive and not self._negative and not self._settings:
            return ImagePromptsData()
        return ImagePromptsData(positive=self._positive,
                                negative=self._negative,
                                settings=self._settings,
                                raw=self._raw,
                                raw_without_settings=self._raw_without_settings
                                )


if __name__ == '__main__':
    for path in [
        # '1.png',
        # '2(loss).png',
        # '3(encode).jpg',
        # '4(real).jpg',
        # '5(drawthings).png',
        # 'tt.jpeg'
    ]:
        print('<' * 10, path, '>' * 10)
        path = Path(f'../example/images/{path}')
        img_prompts = ImagePromptInfo(path).prompts
        print(img_prompts.raw)
        # print(img_prompts.positive)
        # print(img_prompts.negative)
        print('_' * 80)
