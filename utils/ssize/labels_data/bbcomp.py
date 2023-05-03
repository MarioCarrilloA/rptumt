import csv
import glob
import matplotlib.pyplot as plt

def avg_box_areas(label_files, bsize):
    """
    This function calculate the average areas of the
    predicted bounding boxes
    """
    areas = []
    counter = 0
    gcounter = 1
    with open(bsize + ".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        print("Computing areas of input files...")
        for label_file in label_files:
            f = open(label_file, 'r')
            labels = f.readlines()
            f.close()
            for label in labels:
                (cathegory, xc, yc, w, h) = label.strip().split(" ")
                area = 0.0
                area = float(w) * float(h)
                areas.append(area)
                if (counter == 0):
                    writer.writerow([gcounter, area, label_file])
                else:
                    writer.writerow([gcounter, area])
                counter+=1
                gcounter+=1
            counter=0
    print("Total labels found: " + str(len(areas)))
    return sum(areas) / len (areas)


b90um = glob.glob("90um/exp2/labels/*.txt")
b200um = glob.glob("200um/exp3/labels/*.txt")
b355um = glob.glob("355um/exp4/labels/*.txt")
b500um = glob.glob("500um/exp5/labels/*.txt")

print("Beads 90um")
avgb90um = avg_box_areas(b90um, "90um")
pxavgb90um = (avgb90um * (1280*720))/1
print(avgb90um)
print(pxavgb90um)
print("--------------------------\n")

print("Beads 200um")
avgb200um = avg_box_areas(b200um, "200um")
pxavgb200um = (avgb200um * (1280*720))/1
print(avgb200um)
print(pxavgb200um)
print("--------------------------\n")

print("Beads 355um")
avgb355um = avg_box_areas(b355um, "355um")
pxavgb355um = (avgb355um * (1280*720))/1
print(avgb355um)
print(pxavgb355um)
print("--------------------------\n")

print("Beads 500um")
avgb500um = avg_box_areas(b500um, "500um")
pxavgb500um = (avgb500um * (1280*720))/1
print(avgb500um)
print(pxavgb500um)


x = [r'$500-600\mu m$', r'$355-425\mu m$', r'$200-300\mu m$', r'$90\mu m$']
y = [avgb500um, avgb355um, avgb200um, avgb90um]
plt.bar(x, y)
plt.title('Beads -  bounding box areas')
plt.xlabel('Bead type')
plt.ylabel('Average bounding box area - normalized [0,1]')
plt.savefig('Bbox_areas.png')

x = [r'$500-600\mu m$', r'$355-425\mu m$', r'$200-300\mu m$', r'$90\mu m$']
y = [pxavgb500um, pxavgb355um, pxavgb200um, pxavgb90um]
plt.bar(x, y)
plt.title('Beads -  bounding box areas')
plt.xlabel('Bead type')
plt.ylabel('Average bounding box area - number of pixels')
plt.savefig('Pixels_box_areas.png')
