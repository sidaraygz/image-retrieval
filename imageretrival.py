import imageio as iio
import os



def createempty(w, h):
    arr = [[0 for x in range(w)] for y in range(h)]
    return arr


def rgbtogray(img, imgh, imgw):
    grayimage = createempty(imgw, imgh)
    for i in range(imgh):
        for j in range(imgw):
            grayimage[i][j] = int(img[i][j][0] * 0.299 + img[i][j][1] * 0.587 + img[i][j][2] * 0.114)
    return grayimage


def hist(img, imgh, imgw):
    histo = [0 for x in range(256)]
    for i in range(1, imgh - 1, 1):
        for j in range(1, imgw - 1, 1):
            val = unilbp(img, i, j)
            histo[val] += 1
    return histo


def unihistogram(f):
    img = iio.imread(f)
    # Output img with window name as 'image'
    imgh = len(img)
    imgw = len(img[0])
    grayimg = rgbtogray(img, imgh, imgw)
    unihist = hist(grayimg, imgh, imgw)
    a = normalize(unihist)
    cleanhist = clean(a)
    return cleanhist


def clean(histo):
    liste = [0 for x in range(59)]
    i = 0
    for idx, item in enumerate(histo):
        if item != 0 and idx != 59:
            liste[i] = item
            i += 1
        elif idx == 59:
            liste[58] = item
    return liste


def normalize(liste):
    tmp = [0 for x in range(256)]
    for i in range(256):
        tmp[i] = (liste[i] - min(liste)) / (max(liste) - min(liste))
    return tmp


def unilbp(img, i, j):
    binary = 0
    contgreg = 0
    if img[i][j] <= img[i - 1][j - 1]:
        binary += 128
    if img[i][j] <= img[i - 1][j]:
        binary += 64
    if img[i][j] <= img[i - 1][j + 1]:
        binary += 32
    if img[i][j] <= img[i][j - 1]:
        binary += 16
    if img[i][j] <= img[i][j + 1]:
        binary += 8
    if img[i][j] <= img[i + 1][j - 1]:
        binary += 4
    if img[i][j] <= img[i + 1][j]:
        binary += 2
    if img[i][j] <= img[i + 1][j + 1]:
        binary += 1
    for a in reversed(range(7)):
        if format(binary, '08b')[a] != format(binary, '08b')[a - 1]:
            contgreg += 1
    if contgreg <= 2:
        return binary
    else:
        return 59


def train():
    directory = 'images'
    file = open('train.txt', 'w')

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        cleanhist = unihistogram(f)

        file.write(filename + ': ')
        file.write(' '.join(str(item) for item in cleanhist))
        file.write('\n')


def manhattan(a, b):
    return sum(abs(val1 - float(val2)) for val1, val2 in zip(a, b))


def compare(filename, cleanhist):
    diffs = {}
    print(filename + ":\n")

    with open('train.txt', 'r') as file:
        for line in file:
            diff = manhattan(cleanhist, list(line.split()[1:]))
            diffs[line.split()[0]] = diff
        sortddiff = dict(sorted(diffs.items(), key=lambda item: item[1]))
        for key, value in list(sortddiff.items())[:3]:
            txt = key.replace(":", "")
            print(f"{txt} Mesafe: {value:.2f}")
        print("\n")


def main():
    directory = 'test'
    run = 1
    while run:
        cho = int(input("Dizin icin 1 tek resim icin 2 cıkmak icin 0 giriniz: "))
        imagename = "banded_0025.jpg"
        if cho == 2:
            cleanhist = unihistogram(imagename)
            compare(imagename, cleanhist)

        elif cho == 1:
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                cleanhist = unihistogram(f)
                compare(filename, cleanhist)
        elif cho == 0:
            run = 0


main()
