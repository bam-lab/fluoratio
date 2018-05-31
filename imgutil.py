# Copyright 2018 Johanan Idicula

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from skimage import io, exposure, feature, morphology
from skimage.filters.rank import mean
from skimage import filters
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from copy import deepcopy


# TODO actual background subtraction of input image
def background_subtract(input_img_filepath):
    # Open image
    img = io.imread(input_img_filepath)
    # bilateral smoothing to preserve borders
    img_smooth = mean(img, morphology.disk(10))
    # Equalize histogram of input image
    img_histeq = exposure.equalize_adapthist(img_smooth)
    # Highpass filter for image
    img_otsu = img_histeq >= filters.threshold_otsu(img_histeq)
    # generate mask
    # edges = feature.canny(filters.gaussian(img_histeq),
    #                       sigma=1,
    #                       # low_threshold=0.01*((2**16)-1),
    #                       # high_threshold=0.1*((2**16)-1)
    #                       )
    # mask = ndi.binary_fill_holes(edges)
    # mask = morphology.binary_dilation(mask)
    # mask = ndi.binary_fill_holes(mask)
    # mask = morphology.binary_closing(mask)
    # mask = morphology.binary_opening(mask)
    # mask = ndi.binary_fill_holes(mask)
    mask = ndi.binary_fill_holes(img_otsu)
    return img, img_smooth, img_histeq, img_otsu, mask


def mask_test(input_img_filepath):
    img, img_smooth, img_histeq, img_otsu, mask = background_subtract(input_img_filepath)
    print("img low contrast: " + str(exposure.is_low_contrast(img)))
    print("img_histeq low contrast: " + str(exposure.is_low_contrast(img_histeq)))
    print("img_otsu low contrast: " + str(exposure.is_low_contrast(img_otsu)))
# Generate plot
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(9, 3),
                                                  sharex=True, sharey=True)
    # Display input image
    ax1.imshow(img, cmap=plt.cm.gray)
    ax1.axis("off")
    ax1.set_title("orig", fontsize=12)

    # Display input image
    ax2.imshow(img_smooth, cmap=plt.cm.gray)
    ax2.axis("off")
    ax2.set_title("img_smooth", fontsize=12)

    # Display histeq image
    ax3.imshow(img_histeq, cmap=plt.cm.gray)
    ax3.axis("off")
    ax3.set_title("histeq", fontsize=12)

    # Display otsu image
    ax4.imshow(img_otsu, cmap=plt.cm.gray)
    ax4.axis("off")
    ax4.set_title("otsu", fontsize=12)
    # Display mask
    ax5.imshow(mask, cmap=plt.cm.gray)
    ax5.axis("off")
    ax5.set_title("mask", fontsize=12)

    fig.tight_layout()
    plt.show()


for i in range(11, 13):
    position_num = str('{:03d}'.format(i))
    test_filepath = "/Users/johanan/prog/test/Mark_and_Find_001/Position" + position_num + "/Position" + position_num + "_t35_ch00.tif"
    mask_test(test_filepath)
# test_img_filepath = "/Users/johanan/prog/test/Mark_and_Find_001/Position002/Position002_t35_ch00.tif"
# mask_test(test_img_filepath)
