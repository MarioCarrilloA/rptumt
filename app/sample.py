import random
import string
import cv2


class Sample():
    """
    Class to save information about every sample (image) that is
    processed by YOLOv5
    """
    def __init__(self, identity="undefined"):
        self.identity = identity
        self.sample_path = "undefined"
        self.total_bboxes = 0
        self.mean = 0.0
        self.sd = 0.0
        self.areas = []
        self.estimated_size = 0.0
        self.image_name = "sample.png"
        self.status = "INVALID"


    def load_sample_image(self):
        """
        Reads an image from the path that was defined when this
        is created with this class in order to be processed-
        """
        if self.sample_path == "undefined":
            return None
        img = cv2.imread(self.sample_path + "/" + self.image_name)
        return img


    def load_predicted_image(self):
        """
        Loads the predecited image which is the output of YOLOv5
        """
        if self.sample_path == "undefined":
            return None

        # TODO: Remove hardcode and add support to specify this output
        # path by using a YAML configuration file.
        img = cv2.imread(self.sample_path + "/prediction/" + self.image_name)
        return img
