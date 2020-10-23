import cv2
import numpy as np 
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--webcam', help="True/False", default=False)
parser.add_argument('--play_video', help="Tue/False", default=False)
parser.add_argument('--image', help="Tue/False", default=False)
parser.add_argument('--video_path', help="Path of video file", default="videos/car_on_road.mp4")
parser.add_argument('--image_path', help="Path of image to detect objects", default="Images/bicycle.jpg")
parser.add_argument('--verbose', help="To print statements", default=True)
args = parser.parse_args()

#Load yolo
def load_yolo():
	net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
	classes = []
	with open("coco.names", "r") as f:
		classes = [line.strip() for line in f.readlines()]

	layers_names = net.getLayerNames()
	output_layers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
	colors = np.random.uniform(0, 255, size=(len(classes), 3))
	return net, classes, colors, output_layers

def load_image(img_path):
	# image loading
	img = cv2.imread(img_path)
	img = cv2.resize(img, None, fx=0.4, fy=0.4)
	height, width, channels = img.shape
	return img, height, width, channels

def start_webcam():
	cap = cv2.VideoCapture(0)

	return cap


def display_blob(blob):
	'''
		Three images each for RED, GREEN, BLUE channel
	'''
	for b in blob:
		for n, imgb in enumerate(b):
			cv2.imshow(str(n), imgb)

def detect_objects(img, net, outputLayers):			
	blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return blob, outputs

def get_box_dimensions(outputs, height, width):
	boxes = []
	confs = []
	class_ids = []
	for output in outputs:
		for detect in output:
			scores = detect[5:]
			class_id = np.argmax(scores)
			conf = scores[class_id]
			if conf > 0.3:
				center_x = int(detect[0] * width)
				center_y = int(detect[1] * height)
				w = int(detect[2] * width)
				h = int(detect[3] * height)
				x = int(center_x - w/2)
				y = int(center_y - h / 2)
				boxes.append([x, y, w, h])
				confs.append(float(conf))
				class_ids.append(class_id)
	return boxes, confs, class_ids
			
def draw_labels(boxes, confs, colors, class_ids, classes, img): 
	indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
	font = cv2.FONT_HERSHEY_PLAIN
	for i in range(len(boxes)):
		if i in indexes:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			color = colors[i]
			cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
			cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
	cv2.imshow("Image", img)

def image_detect(img_path): 
	model, classes, colors, output_layers = load_yolo()
	image, height, width, channels = load_image(img_path)
	blob, outputs = detect_objects(image, model, output_layers)
	boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
	print(class_ids)
	draw_labels(boxes, confs, colors, class_ids, classes, image)
	while True:
		key = cv2.waitKey(1)
		if key == 27:
			break

def webcam_detect():
	model, classes, colors, output_layers = load_yolo()
	cap = start_webcam()
	while True:
		_, frame = cap.read()
		height, width, channels = frame.shape
		blob, outputs = detect_objects(frame, model, output_layers)
		boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
		draw_labels(boxes, confs, colors, class_ids, classes, frame)
		key = cv2.waitKey(1)
		if key == 27:
			break
	cap.release()


def start_video(video_path):
	global boxes, confs, class_ids, p0, frame

	model, classes, colors, output_layers = load_yolo()
	cap = cv2.VideoCapture(video_path)

	
	while True:
		_, frame = cap.read()
		height, width, channels = frame.shape
		blob, outputs = detect_objects(frame, model, output_layers)
		boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
		draw_labels(boxes, confs, colors, class_ids, classes, frame)
		if 0 in class_ids:	# Person class found
			break
		key = cv2.waitKey(1)
		if key == 27:
			break

	old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	p0 = cv2.goodFeaturesToTrack(old_gray, 100, 0.01, 10, None, None, 7)
	index = 0
	for i in ( p0 ):
		print(p0)
		print(len(p0), "\n")
		for box in boxes:
			x, y, w, h = box
			if (i[0][0] < x) or (i[0][0] > x + w) or (i[0][1] < y) or (i[0][1] > y + h):
				if index < len(p0):
					p0 = np.delete(p0, index, axis=0)
			else:
				index = index + 1
	while True:
		_, frame = cap.read()
		height, width, channels = frame.shape
		blob, outputs = detect_objects(frame, model, output_layers)
		boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
		draw_labels(boxes, confs, colors, class_ids, classes, frame)
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)		
		p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None,
												None, None,
												(30, 30), 2,
												(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
		good_p1 = p1[st==1]
		maxAll = np.amax(good_p1, axis = 0)
		minAll = np.amin(good_p1, axis = 0)
		maxX  =  maxAll [ 0 ] # [0]
		maxY  =  maxAll [ 1 ] # [1]
		minX = minAll[0]#[0]
		minY  =  minAll [ 1 ] # [1]

		for  i , ( f2 , f1 ) in  enumerate ( zip ( p1 , p0 )):
			a, b = f2.ravel()
			c, d = f1.ravel()
			cv2.circle(frame, (a, b), 5, (255, 255, 0), -1)
			cv2.circle(frame, (c, d), 5, (255, 0, 0), -1)
			cv2.line(frame, (a, b), (c, d), (0,0,255), 2)

		frame_final_gray = np.copy(frame_gray)
		p0 = cv2.goodFeaturesToTrack(frame_final_gray, 100, 0.01, 10, None, None, 7)
		index2 = 0
		for  p  in ( p0 ):
			if (p[0][0] < (np.int0(minX) -2) or p[0][0] > (np.int0(maxX) +2)) or (p[0][1] < (np.int0(minY)-2) or p[0][1] > (np.int0(maxY)+2)):
				p0 = np.delete(p0, index2, axis=0)
			else:
				index2 = index2 + 1

		if len(p0)<10:
			cv2.rectangle(frame_gray, (np.int0(minX), np.int0(minY)), (np.copy(maxX), np.int0(maxY)), (0, 255, 0), 2)
			p0 = cv2.goodFeaturesToTrack(frame_final_gray, 100, 0.01, 10, None, None, 7)
			index3 = 0
			for g in (p0):
				if ((g[0][0] < (minX - 20)) or (g[0][0] > (maxX + 20))) or ((g[0][1] < (minY - 20)) or (g[0][1] > (maxY + 20))):
					p0 = np.delete(p0, index3, axis=0)
				else:
					index3 = index3 + 1


	cap.release()


if __name__ == '__main__':


	# if webcam:
	# 	if args.verbose:
	# 		print('---- Starting Web Cam object detection ----')
	# 	webcam_detect()


	video_path = "videos/pedestrians.mp4"
	if args.verbose:
		print('Opening '+video_path+" .... ")
	start_video(video_path)


	# if image:
	# image_path = "Images/busy_street.jpg"
	# if args.verbose:
	# 	print("Opening "+image_path+" .... ")
	# image_detect(image_path)
	

	cv2.destroyAllWindows()