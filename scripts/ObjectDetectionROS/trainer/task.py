from pytorchyolo import train
import os

if __name__ == "__main__":
    path_to_script = os.path.dirname(__file__) + "/data/get_coco_dataset.sh"
    os.system("bash " + path_to_script)
    train.run()
