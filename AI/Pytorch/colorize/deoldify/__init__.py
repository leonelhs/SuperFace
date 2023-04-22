import sys
import logging

from AI.Pytorch.colorize.deoldify._device import _Device

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)


device = _Device()
