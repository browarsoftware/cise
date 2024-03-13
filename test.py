# Jinja2 language
# https://maplibre.org/maplibre-gl-js/docs/examples/
#from distutils.log import debug
#from fileinput import filename
from flask import *
import os
import uuid
from io import BytesIO
import base64
from PIL import Image
import pickle

############################################################################

import numpy as np
import cv2
from sklearn.metrics.pairwise import pairwise_distances

how_many_to_find = 16
path_to_results = 'data/'
path_to_data = 'd:/data/credo/data/'
change_path = True
# processing: BORDER_REFLECT101

uploaded_dir = 'static/uploaded'
isExist = os.path.exists(uploaded_dir)
if not isExist:
   os.makedirs(uploaded_dir)
   print("The new directory is created!")

print("Loading embedding")
emb_array = np.load(path_to_results + "/embedding.npy")
my_file = open(path_to_results + "/files_names.txt", "r")
file_content = my_file.read()
all_files = file_content.split("\n")
how_many_images = 573335

v_correct = np.load(path_to_results + "/v_st.npy")
mean_face = np.load(path_to_results + "/mean_face.npy")

with open(path_to_results + '/all_data_dic.pickle', 'rb') as handle:
    all_data_dict = pickle.load(handle)
print("Done")

from sklearn.decomposition import PCA
from math import atan2
import math
def align_image_2(img, borderMode = cv2.BORDER_CONSTANT):
    src_copy = np.copy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_copy = np.copy(gray)
    my_list = []
    for x in range(gray.shape[0]):
        for y in range(gray.shape[1]):
            z = 0
            while z < gray[x,y]:
                my_list.append([y, x])
                z = z + 1

    X = np.array(my_list)
    pca = PCA(n_components=2)
    pca.fit(X)
    mean = pca.mean_
    eigenvectors = pca.components_

    cntr = (int(mean[0]), int(mean[1]))
    angle = atan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians
    angle = 180 * angle / math.pi

    (cX, cY) = cntr
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    (h, w) = src_copy.shape[:2]

    rotated = cv2.warpAffine(src_copy, M, (w, h), borderMode = borderMode)

    xx = w / 2 - cX
    yy = h / 2 - cY
    M = np.float32([[1, 0, xx], [0, 1, yy]])

    shifted = cv2.warpAffine(rotated, M, (rotated.shape[1], rotated.shape[0]), borderMode = borderMode)

    return shifted

def embedding(carrier_img_i, v, mean_face):
    carrier_img = np.copy(carrier_img_i)
    img_flat = carrier_img.flatten('F')
    img_flat -= mean_face
    result = np.matmul(v.transpose(), img_flat)
    return result



############################################################################

def create_random_file_name():
    return str(uuid.uuid4())

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def main2():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        how_many_to_search = int(request.form['count'])
        how_many_to_find = how_many_to_search
        #f.save(f.filename)
        file_name = uploaded_dir + '/' + create_random_file_name() + '.png'
        f.save(file_name)
        file_name_temp = file_name

        #yy = np.expand_dims(emb_array[i,], axis=0)
        full_path = file_name
        # img_help = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
        img_help = cv2.imread(full_path, cv2.IMREAD_COLOR)
        if img_help.shape[0] != 60 or img_help.shape[1] != 60:
            img_help = cv2.resize(img_help, (60, 60))
        shifted = align_image_2(img_help, borderMode=cv2.BORDER_REFLECT101)
        shifted = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)

        embed = embedding(shifted / 255, v_correct, mean_face)
        #yy = np.expand_dims(embed[0:dim_count], axis=0)
        yy = np.expand_dims(embed, axis=0)
        ww = pairwise_distances(X=emb_array, Y=yy, n_jobs=-1)
        ww = ww[:, 0]
        indexes = np.argsort(ww)
        dist_sort = ww[indexes]

        #my_ids = indexes[0:how_many_to_find + 1]
        #dist_sort = dist_sort[0:how_many_to_find + 1]
        my_ids = indexes[0:how_many_to_find]
        dist_sort = dist_sort[0:how_many_to_find]

        # print(my_ids)
        # print(dist_sort)

        files_paths = []
        files_bin = []
        lon = []
        lat = []
        for aaa in range(len(my_ids)):
            file_name = path_to_data + all_files[my_ids[aaa]]
            # path mapping to show not original images, not aligned ones
            #if change_path:
            #    file_name = file_name.replace('d:/data/credo/align_BORDER_REFLECT101/', 'd:/data/credo/data/')
            files_paths.append(file_name)
            val = file_name
            while val.find('/') >= 0:
                val = val[(val.find('/')+1):]
            val = val[:val.find('.')]
            val = int(val)
            if val in all_data_dict.keys():
                val_dict = all_data_dict[val]
                lon.append(val_dict['lon'])
                lat.append(val_dict['lat'])
                # print(str(val_dict['lon']) + " " +  str(val_dict['lat']))

            else:
                lon.append(0)
                lat.append(0)
            xxx = 1
            xxx = xxx + 1

        # Get query image
        img = Image.fromarray(img_help)
        with BytesIO() as buf:
            img.save(buf, 'jpeg')
            image_bytes = buf.getvalue()
        encoded_string = base64.b64encode(image_bytes).decode()
        files_bin.append(encoded_string)

        #file_name = 'd:/data/credo/align_BORDER_REFLECT101/worms/2/33990350.png'
        for ff in files_paths:
            img = Image.open(ff)
            with BytesIO() as buf:
                img.save(buf, 'jpeg')
                image_bytes = buf.getvalue()
            encoded_string = base64.b64encode(image_bytes).decode()
            files_bin.append(encoded_string)
        os.remove(file_name_temp)
        dist_sort_str = ["{:.3f}".format(v) for v in dist_sort]
        dist_sort_str.insert(0, "{:.3f}".format(0))
        #print(lon)
        #print(lat)
        #return render_template('images.html', img_data0=files_bin[0], img_data1=files_bin[1], img_data2=files_bin[2], img_data3=files_bin[3]), 200
        return render_template('images.html', img_data=files_bin, credo_hit_dist=dist_sort_str,lon=lon,lat=lat), 200
        #return render_template('images_with_map.html', img_data=files_bin, credo_hit_dist=dist_sort_str, lon=lon, lat=lat), 200
        """
        #return render_template("acknowledgement.html", name=file_name)
        binderList = os.listdir(uploaded_dir)
        binderList = ['uploaded/' + image for image in binderList]
        return render_template("many_images.html", binderList=binderList)
        """


if __name__ == '__main__':
    app.run(debug=True)

