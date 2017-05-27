#!/usr/bin/python

import numpy as np
import os
import skimage.color as color
import matplotlib.pyplot as plt
import scipy.ndimage.interpolation as sni
import caffe
import argparse
import notifier

def colorize(id, token):
	prototxt = "./neuralnet/deploy.prototxt";
	caffemodel = "./neuralnet/release.caffemodel"

	input_path = "./storage/input/"
	output_path = "./storage/output/"
	img_in = input_path + id + ".png"
	img_out = output_path + id + ".png"
	
	caffe.set_mode_cpu()

	net = caffe.Net(prototxt, caffemodel, caffe.TEST)

	(H_in, W_in) = net.blobs['data_l'].data.shape[2:]
	(H_out, W_out) = net.blobs['class8_ab'].data.shape[2:]

	#pts_in_hull = np.load('./neuralnet/resource.npy')
	#net.params['class8_ab'][0].data[:, :, 0, 0] = pts_in_hull.transpose((1, 0))

	img_rgb = caffe.io.load_image(img_in)

	img_lab = color.rgb2lab(img_rgb)
	img_l = img_lab[:, :, 0]
	(H_orig, W_orig) = img_rgb.shape[:2]

	img_rs = caffe.io.resize_image(img_rgb, (H_in, W_in))
	img_lab_rs = color.rgb2lab(img_rs)
	img_l_rs = img_lab_rs[:, :, 0]

	net.blobs['data_l'].data[0, 0, :, :] = img_l_rs - 50
	net.forward()

	ab_dec = net.blobs['class8_ab'].data[0, :, :, :].transpose((1, 2, 0))
	ab_dec_us = sni.zoom(ab_dec, (1.*H_orig / H_out, 1.*W_orig / W_out, 1))
	img_lab_out = np.concatenate((img_l[:, :, np.newaxis], ab_dec_us), axis = 2)
	img_rgb_out = (255 * np.clip(color.lab2rgb(img_lab_out), 0, 1)).astype('uint8')

	plt.imsave(img_out, img_rgb_out)

	notifier.notify(id, token)
