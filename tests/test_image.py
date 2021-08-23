import tensorflow as tf
import imgaug as ia
import deepdanbooru as dd
import numpy as np

def test_image_augment():
    # ia.seed(3)
    img1 = tf.keras.preprocessing.image.load_img('tests\\images\\image1.jpg')
    n_img1 = tf.keras.preprocessing.image.img_to_array(img1, dtype=np.uint8)
    aug = dd.image.augment()
    # print(aug)
    # aug = ia.augmenters.Flipud(1)

    o_img1 = aug(image=n_img1)
    print(o_img1)
    print(o_img1.shape)

    tf.keras.preprocessing.image.save_img('tests\\images\\o_image1.jpg', o_img1, scale=False, quality=100)
