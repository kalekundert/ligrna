from PIL import Image
im = Image.open('20170111_test_cf_spacers_in_vitro.tif')
#im.show()

import numpy as np
from matplotlib.pyplot import imshow
imshow(np.asarray(im))
