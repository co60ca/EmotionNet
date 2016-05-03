import numpy as np
#import matplotlib.pyplot as plt
import json
import caffe

import csv

import sys
import os
caffe_root = './'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')

caffe.set_mode_cpu()

net = None
transformer = None

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
def setup(model_def, model_weights):
    global net
    global transformer
    model_def = caffe_root + model_def
    #model_weights = caffe_root + 'snapshots/ggn_full_crop_iter_56000.caffemodel'
    model_weights = caffe_root + model_weights

    net = caffe.Net(model_def,      # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)     # use test mode (e.g., don't perform dropout)

    mu = np.array([127,127,127])

    # create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
    transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
    transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR
    net.blobs['data'].reshape(50,        # batch size
                              3,         # 3-channel (BGR) images
                              227, 227)  # image size is 227x227

def defaults():
    setup('ggn-net/deploy.prototxt', 'snapshots/ggn_full_crop_halfface_iter_56000.caffemodel')


cursize = 50
def resize(ournet, size, oldsize):
    if oldsize != size:
        ournet.blobs['data'].reshape(size, 3, 227, 227)
        cursize = size

def class_img(img):
    resize(net, 1, cursize)
    image = caffe.io.load_image(img)
    transformed_image = transformer.preprocess('data', image)
    #plt.imshow(image)

    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[0] = transformed_image

    ### perform classification
    output = net.forward()

    #print output

    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

    print output_prob

    #print 'predicted class is:', output_prob.argmax()
    return json.dumps({"class": output_prob.argmax(),
                      "output_prob": output_prob.tolist()})

def class_imgs(list_img):
    """
    Classify all images in a python list

    Keyword arguements:
    list_img -- List of files relative to the current working directory
    """
    numberimg = len(list_img)
    resize(net, numberimg, cursize)
    i = 0
    for img in list_img:
        image = caffe.io.load_image(img)
        transformed_image = transformer.preprocess('data', image)
        net.blobs['data'].data[i] = transformed_image
        i = i + 1

    output = net.forward()

    results = []
    for n in range(0, numberimg):
        themax = output['prob'][n].argmax()
        results.append({'filename':list_img[n], 'class': themax, 'prob': output['prob'][n].tolist()})

    return results

def class_imgs_to_csv(input, stream):
    writer = csv.writer(stream, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['filename', 'class', 'prob0', 'prob1',
                    'prob2', 'prob3', 'prob4', 'prob5',
                    'prob6', 'prob7'])
    for result in input:
        row = [result['filename'], result['class']]
        row.extend(result['prob'])
        writer.writerow(row)

def all_dir(imgdir):
    """
    Classify all images in one directory

    Keyword arguements:
    imgdir -- string containing relative path to images
    """
    output = []
    maxbatch = 50
    batch = []
    for root, dirs, files in os.walk(imgdir):
        for filename in files:
            batch.append(imgdir + "/" + filename)
            if len(batch) == maxbatch:
                output.extend(class_imgs(batch))
                batch = []
    if len(batch) != 0:
        output.extend(class_imgs(batch))
    return output
