#import detect

from yolov5_upstream import detect

detect.run(
        weights="BEADS_DATA/weights/best.pt",
        source="BEADS_DATA/Tests/*.png",
        hide_conf=True,
        hide_labels=True,
        line_thickness=1,
        save_txt=True
)
