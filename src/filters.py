from skimage.filters import gaussian

# Sigma for the blur filter (the bigger it is the more blurry the footage will be)
BLUR_SIGMA = 5

def blur(image):
    """ Returns a blurred version of the image """
    return gaussian(image.astype(float), sigma=BLUR_SIGMA)
