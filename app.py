from flask import Flask, render_template, request
import math
import jsonify
import requests
import numpy as np
import pandas as pd
import base64
import io
import matplotlib.image as mpimg
from PIL import Image
from sklearn.decomposition import PCA

app = Flask(__name__)
app.secret_key = "super secret key"

def normalize(x):
    """
    Normalize a list of sample image data in the range of 0 to 1,
    x: List of image data.  The image shape is (width, height, 3),
    return: Numpy array of normalized data
    """
    return np.array((x - np.min(x)) / (np.max(x) - np.min(x)))


def compressImage(file):
    image = mpimg.imread(file)
    # Splitting the RED, BLUE and GREEN channels
    r,g,b = image[:,:,0],image[:,:,1],image[:,:,2]

    minSize = min(image.shape[0],image.shape[1])
    n_components = [50]

    for i in range(len(n_components)):
        # RED
        pca_r = PCA(n_components=n_components[i])
        pca_r.fit(r)
        tpca_r = pca_r.transform(r)

        # Green
        pca_g = PCA(n_components=n_components[i])
        pca_g.fit(g)
        tpca_g = pca_g.transform(g)

        # Blue
        pca_b = PCA(n_components=n_components[i])
        pca_b.fit(b)
        tpca_b = pca_b.transform(b)

        # The data of the image is fit and principal components are generated,
        # Now inverse_transform the transformed data to generate the compressed image.
        r_reduced = pca_r.inverse_transform(tpca_r)
        b_reduced = pca_b.inverse_transform(tpca_b)
        g_reduced = pca_g.inverse_transform(tpca_g)

        compressed = np.dstack((r_reduced,g_reduced,b_reduced))

        compressed = normalize(compressed)
        compressedImage = Image.fromarray((compressed * 255).astype(np.uint8))
        
        data = io.BytesIO()
        compressedImage.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())

    return render_template('index.html', img_data=encoded_img_data.decode('utf-8'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html', hidden="hidden")

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return render_template('index.html')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html')
    if file:
        return compressImage(file)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)