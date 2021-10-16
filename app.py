from flask import Flask, render_template, request
import math
import jsonify
import requests
import numpy as np
import pandas as pd
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


def compressImage():
    imagepath = "static/original.jpg"
    image = mpimg.imread(imagepath)
    # Splitting the RED, BLUE and GREEN channels
    r,g,b = image[:,:,0],image[:,:,1],image[:,:,2]

    minSize = min(image.shape[0],image.shape[1])
    n_components = [math.ceil(.4*minSize),math.ceil(.6*minSize),math.ceil(.8*minSize)]

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
        compressedImage.save(f"static/ci{i+1}.jpeg")

    return 0

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file.save("static/original.jpg")
        compressImage()
        return render_template('index.html')
    else:
        return redirect(request.url)

if __name__=="__main__":
    app.run(debug=True)