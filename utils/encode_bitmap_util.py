from wx.tools import img2py
import os


class EncodeBitmapsUtil:
    def __init__(self, images_dir_, target_file):
        self.images_dir = images_dir_
        self.target_file = target_file

    def run(self):
        is_first = True

        for root, directories, files in os.walk(self.images_dir):
            for image in files:
                relative_path = os.path.relpath(os.path.join(root, image), ".")
                file_name = image.split('.')[0]
                if is_first:
                    arg_str = "-F -n {} {} {}".format(file_name, relative_path, self.target_file)
                    is_first = False
                else:
                    arg_str = "-a -F -n {} {} {}".format(file_name, relative_path, self.target_file)
                img2py.main(arg_str.split())


if __name__ == '__main__':
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    images_dir = os.path.join(root_path, 'assets', 'images')
    target_image_file = os.path.join(root_path, 'images.py')
    EncodeBitmapsUtil(images_dir, target_image_file).run()