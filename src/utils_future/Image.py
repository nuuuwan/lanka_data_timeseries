
from PIL import Image as PILImage
from utils import Log

from utils_future.Point2D import Point2D
from utils_future.Size2D import Size2D

log = Log(__name__)


class Image:
    def __init__(self, im: PILImage.Image):
        self.im = im

    @staticmethod
    def load(image_path: str):
        return Image(PILImage.open(image_path))

    def write(self, image_path: str):
        self.im.save(image_path)
        log.debug(f'Saved {image_path}')
        return image_path

    @property
    def size(self):
        return self.im.size

    def crop(
        self,
        lefttop: Point2D,
        widthheight: Size2D,
    ):
        bbox = lefttop.to_tuple() + (lefttop + widthheight).to_tuple()
        im = self.im.crop(bbox)
        log.debug(f'Cropped image to {lefttop} and {widthheight}')
        return Image(im)

    def resize(self, ratio: float):
        im = self.im
        width, height = im.size
        newsize = (int(width * ratio), int(height * ratio))
        im = im.resize(newsize)
        log.debug(f'Resized image by {ratio} to size({newsize})')
        return Image(im)
