# FaceRecognition

The Haar Cascades for face detection are NOT mine and can be found in [OpenCV's GitHub repository](https://github.com/opencv/opencv/tree/master/data/haarcascades)  

The Shape Predictor pre trained model is NOT mine and can be found in [Davisking's dlib-models GitHub repository](https://github.com/davisking/dlib-models)  

The Face Recognition pre trained model is NOT mine and can be found in [Davisking's dlib-models GitHub repository](https://github.com/davisking/dlib-models)  

## Features

### Identify the actors detected in an image

### :warning::exclamation: The names of the movies are in Portuguese - known issue - being fixed :exclamation::warning:

#### Example 1 - Tom Cruise - in Mission Impossible 4 and in IMDB

	Identifies Tom Cruise in Mission Impossible 4 (left picture) and in the his IMDB page (rigth, used to encode 
	his face the first time).

![Example1](https://raw.githubusercontent.com/RafaelRibeiro97/FaceRecognition/master/media/Example1.png)


### List the movies / series the detected actor have been together

#### Example 2 - Alexandra Daddario (in Baywatch)  

	Identifies Alexandra Daddario in Baywatch and lists the movies she's been in.
:warning::exclamation: The names of the movies are in Portuguese - known issue - being fixed :exclamation::warning:

![Example2](https://raw.githubusercontent.com/RafaelRibeiro97/FaceRecognition/master/media/Example2.PNG)

#### Example 3 - Gal Gadot and Vin Diesel

	Identifies Gal Gadot and Vin Diesel and lists the movies they've been in.
:warning::exclamation: The names of the movies are in Portuguese - known issue - being fixed :exclamation::warning:

![Example3](https://raw.githubusercontent.com/RafaelRibeiro97/FaceRecognition/master/media/Example3.PNG)

### :warning::exclamation: The names of the movies are in Portuguese - known issue - being fixed :exclamation::warning:


## Requirements
	* mss 				- Screen capture
	* Numpy 			- Matrix calculations
	* CSV				- Data storing and loading
	* CV2				- Image rendering
	* Dlib				- Face recognition
	* requests			- HTTP requests
	* BeautifulSoup 		- Image download
Download mss from [BoboTig's GitHub repository](https://github.com/BoboTiG/python-mss)
	
## How to use
#### Download the pictures of the first X actors / actresses in IMDB
```python
#Set IMAGES_TO_DONWLOAD in IMDBActors.py:11 to the number of images to be downloaded.
IMAGES_TO_DONWLOAD = 100 #Number of images to download. MUST BE A MULTIPLE OF 50. 
```

```bash
#Run the script to download the images. The images will be donwloaded to a folder with
#the name 'actors' created by the script in the same directory.
$ python IMDBActors.py
```
#### Run FaceDetection.py to detect all the faces on the screen. Only the top corner (0, 0) to (800, 600) is detected.
```bash
#Run the script to identify the actors / actresses. The movies / series where
#they have been together are listed in the terminal.
$ python FaceDetection.py
```

## :warning::warning:Known issues
	* The names of the movies are in Portuguese;

## :heavy_check_mark::heavy_check_mark:Previously known issues - SHOULD be fixed now
	* When a face is detected but the reply from IMDB is not expected, the program crashes;

