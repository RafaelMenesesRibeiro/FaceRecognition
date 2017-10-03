import os, time, errno
import mss #https://python-mss.readthedocs.io/en/dev/examples.html
import numpy as np
import csv
import cv2
import dlib
import IMDBActors as imdb

MONITOR = {'top': 0, 'left': 0, 'width': 800, 'height': 600}

def capture(sct):
	return sct.grab(MONITOR)

KNEWFACES_DIR = 'Resources/KnownPeopleToEncode'
KFACES_DIR = 'Resources/KnownPeople'
KFACES_FILEPATH = 'Resources/KnownEncodings.csv'
KPEOPLE = []

'''
Reads the .csv file that contains all the saved known pairs (name, encoding).
Adds each pair to KPEOPLE array.

input:	no input
output:	no output
'''
def kFacesRead():
	#If the file exists - loads the saved known pairs (name, encoding).
	try:
		print('Trying to load saved known encodings...')
		#Opens the .csv file that contains all the saved known pairs (name, encoding).
		with open(KFACES_FILEPATH, 'r') as csvfile:
			reader = csv.reader(csvfile) #Inits the reader.
			failedFaces = 0
			totalFaces = 0
			for row in reader:
				try:
					totalFaces += 1
					#Transforms the string of the numpy array of the enconding to
					#a numpy array.
					encS = row[1]
					encS = encS.split()
					encS[0] = encS[0][1:]
					encS[-1] = encS[-1][:-1]
					encSF = []
					for i, j in enumerate(encS):
						if j == '': continue
						f = float(j)
						encSF.append(f)
					encNP = np.array(encSF, dtype=float)
					#Appends the saved known pair (name, encoding) to the array.
					KPEOPLE.append([row[0], encNP])
				except OSError as e:
					failedFaces += 1
					print(e)
					print('Unable to load face {}'.format(row[0]))
		print('Loaded {} of {} known faces.'.format(totalFaces - failedFaces, totalFaces))
		print('Done loading saved known encodings')
	#If the file does not exist - theres were no saved known pairs (name, encoding).
	except FileNotFoundError as filenotfound:
		print('Did not find any saved known encodings.')

'''
Encodes all the new people's faces found in KNEWFACES_DIR and creates the pair
((name, encoding).
Adds each pair to KPEOPLE array.
Writes each pair to the .csv file that contains all the saved known pairs.
Moves all the new images (found in KNEWFACES_DIR) to the directory where all
the known, already encoded, people's faces's images are.

input:	no input
output:	no output
'''
def kFacesSaveNew():
	#Tries to create the directory to store the images of already encoded faces.
	try:
		os.makedirs(KFACES_DIR)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
	print('\nEncoding and saving new known people...')
	#Opens the .csv file that contains all the saved known pairs (name, encoding).
	with open(KFACES_FILEPATH, 'a', newline = '') as csvfile:
		writer = csv.writer(csvfile) #Inits the writer.
		failedFaces = 0
		totalFaces = 0
		for img in os.listdir(KNEWFACES_DIR):
			totalFaces += 1
			pName = (img.split('.'))[0] #Gets the name.
			print('\tEnconding {}'.format(pName))
			path = os.path.join(KNEWFACES_DIR, img)
			image = cv2.imread(path) #Opens the image.
			#Detects the face.
			try:
				(x, y, w, h) = faceDetector.detectMultiScale(image, 1.3, 5)[0]
				#Transforms the rectangle coordenates to the expected type.
				faceRect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
				#Warp the image so the points are always in the same position.
				faceAligned = facePosePredictor(image, faceRect)
				#Gets the face's encoding.
				faceEncoding = uFaceEncode(image, faceAligned, 1)
				#Appends the saved known pair (name, encoding) to the array.
				KPEOPLE.append([pName, faceEncoding])
				#Writes the new known pair (name, encoding) to the .csv file.
				writer.writerow([pName, faceEncoding])
			except:
				failedFaces += 1
				print('Couldn\'t find face in {}.'.format(img))
			#Moves the image to the directory of images of already encoded faces.
			try:
				newpath = os.path.join(KFACES_DIR, img)
				os.rename(path, newpath)
			except:
				print('Couldn\'t move file - {}.'.format(img))
	print('Encoded {} of {} new faces.'.format(totalFaces - failedFaces, totalFaces))
	print('Done encoding and saving new known people.')

'''
Returns the similarity of the unknown face (that is being detected) with all the
known people's faces.

input:	<numpy.array(128)>uEncoding		Encoding of the unknown detected face.
output:	<array(len(KPEOPLE))>			Distance between the detected face and
										all the know ones.
'''
def kFacesSimilarity(uEncoding):
	if len(KPEOPLE) == 0:
		return [9999]
	return [np.linalg.norm(person[1] - uEncoding) for person in KPEOPLE]

'''
Returns the name of the detected face or 'Face not recognized' if it does not
find a match.

input:	<numpy.array(128)>uEncoding		Encoding of the unknown detected face.
output:	<str>							Name of the detected person or
										'Face not recognized'.
'''
def uFaceGetName(uEncoding):
	#Checks if the distance between the unknown encoding and each of the known
	#encodings is lower than the maximum distance needed to be considered a match.
	#The lower the distance, the more similar the encodings need to be.
	l = [i <= 0.6 for i in kFacesSimilarity(uEncoding)]
	#if True in l: return 1, KPEOPLE[l.index(True)][0]
	#else: return 'Face not recognized.'
	names = []
	for i, tValue in enumerate(l):
		if tValue:
			names.append(KPEOPLE[i][0])
			break #SOLVE - WHEN MULTIPLE NAMES ARE GIVEN, IMDB CANT FIND ID.
	if len(names) == 0:
		names.append('Face not recognized.')
	return '+'.join(names)

'''
Returns encoding of the detected face.

input:	<np.array()>image					Frame where the face was detected.
		<dlib.dlib.full_object_detection'>	Location of the face.
		<int>resampling						Number of times to resample the face.
output:	<numpy.array(128)>					Encoding of the unknown detected face.
'''
def uFaceEncode(image, shape, resampling = 1):
	return np.array(faceEncoder.compute_face_descriptor(image, shape, resampling))


def faceDD(imageRGB, x, y, w, h):
	#Adds a rectangle to the image. Debugging and interface purposes.
	cv2.rectangle(imageRGB, (x, y), (x+w, y+h), (255, 255,255), 2)
	#Transforms the rectangle coordenates to the expected type.
	faceRect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
	#Warp the image so the points are always in the same position.
	shape = facePosePredictor(imageRGB, faceRect)
	#Gets the face's encoding.
	uFaceEncoding = uFaceEncode(imageRGB, shape, 1) #Encodes the face.
	#Gets the face's name.
	uFaceName = uFaceGetName(uFaceEncoding) #Names the face.
	#Adds the name of the face on top of the rectangle in the image.
	#Debugging and interface purposes.
	cv2.putText(imageRGB, uFaceName, (x, y-5), 0, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
	return uFaceName

def main():
	kFacesRead() #Loads all the saved known pairs (name, encoding).
	kFacesSaveNew() #Loads all the new known pairs (name, encoding).
	with mss.mss() as sct:
		ids = []
		previousActorList = []
		while True:
			lastTime = time.time() #Debugging purposes.
			image = np.array(capture(sct)) #Captures the screen.
			imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			#Detects the faces in the image.
			facesDetected = faceDetector.detectMultiScale(image, 1.3, 5)
			
			if len(facesDetected) != 0:
				ids = []
				#For each face detected, indentifies it.
				for (x, y, w, h) in facesDetected:
					name = faceDD(imageRGB, x, y, w, h)
					actorID = str(imdb.getActorID(name))
					ids.append(actorID)

				if ids != previousActorList:
					print('\n\n-------------------------------------------------\n')
					previousActorList = ids
					movies = imdb.getActorsMovies(ids)
					print('\nTotal of {} movies.'.format(len(movies)))
					print('-------------------------------------------------')

			cv2.imshow('image', cv2.cvtColor(imageRGB, cv2.COLOR_RGB2BGR)) #Shows the image (with the identities)

			#print('FPS = {}'.format(1 / (time.time() - lastTime))) #Debugging purposes.
			if cv2.waitKey(1) & 0xFF == ord('q'): break #Exits if 'Q' is pressed.

	cv2.destroyAllWindows()			

faceDetector = cv2.CascadeClassifier('Resources/HaarCascades/haarcascade_frontalface_default_CPU.xml')
predictorModel = 'Resources/TrainedModels/shape_predictor_68_face_landmarks.dat'
facePosePredictor = dlib.shape_predictor(predictorModel)
enconderModel = 'Resources/TrainedModels/dlib_face_recognition_resnet_model_v1.dat'
faceEncoder = dlib.face_recognition_model_v1(enconderModel)

if __name__ == '__main__':
	main()
