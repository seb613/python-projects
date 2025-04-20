from .Input import Input
from .Grayscale import Grayscale
from .Sepia import Sepia
from .Blur import Blur
from .Contour import Contour
from .Detail import Detail
from .EdgeEnhance import EdgeEnhance
from .Emboss import Emboss
from .Sharpen import Sharpen
from .Smooth import Smooth
from .GaussianBlur import GaussianBlur
from .UnsharpMask import UnsharpMask
from .MaxFilter import MaxFilter
from .Binarize import Binarize
from .Dilate import Dilate
from .Erode import Erode

class_map: dict[str, type] = {
    "Input": Input,
    "Grayscale": Grayscale,
    "Sepia": Sepia,
    "Blur": Blur,
    "Contour": Contour,
    "Detail": Detail,
    "EdgeEnhance": EdgeEnhance,
    "Emboss": Emboss,
    "Sharpen": Sharpen,
    "Smooth": Smooth,
    "GaussianBlur": GaussianBlur,
    "UnsharpMask": UnsharpMask,
    "MaxFilter": MaxFilter,
    "Binarize": Binarize,
    "Dilate": Dilate,
    "Erode": Erode,
}

__all__ = [
    "Input",
    "Grayscale",
    "Sepia",
    "Blur",
    "Contour",
    "Detail",
    "EdgeEnhance",
    "Emboss",
    "Sharpen",
    "Smooth",
    "GaussianBlur",
    "UnsharpMask",
    "MaxFilter",
    "Binarize",
    "Dilate",
    "Erode",
]
