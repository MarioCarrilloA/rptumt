import glob
import matplotlib.pyplot as plt

def avg_box_areas(label_files):
    """
    This function calculate the average areas of the
    predicted bounding boxes
    """
    areas = []
    print("Computing areas of input files...")
    for label_file in label_files:
        f = open(label_file, 'r')
        labels = f.readlines()
        f.close()
        for label in labels:
            (cathegory, xc, yc, w, h) = label.strip().split(" ")
            area = float(w) * float(h)
            areas.append(area)
    return sum(areas) / len (areas)


labeldir = "./labels"
b200mm = glob.glob(labeldir + "/image_200mm_*")
b500mm = glob.glob(labeldir + "/image_500mm*")
bhydgl = glob.glob(labeldir + "/image_hyd*")

avgb200mm = avg_box_areas(b200mm)
avgb500mm = avg_box_areas(b500mm)
avgbhydgl = avg_box_areas(bhydgl)

print("*** Results ***")
print(avgb500mm)
print(avgb200mm)
print(avgbhydgl)

x = [r'$500\mu m$', r"$200\mu m$", "Hdrgel"]
y = [avgb500mm, avgb200mm, avgbhydgl]
plt.bar(x, y)
plt.title('Beads -  bounding box areas')
plt.xlabel('Bead type')
plt.ylabel('Average bounding box area - normalized [0,1]')
plt.savefig('bbox_areas.png')
