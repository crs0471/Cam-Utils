
# Cam Utils

Verious usefull scripts which was created using opencv, pyautogui, python etc.

### Tech

Cam Utils uses a number of open source projects to work properly:

- [Python] - Code langage for write scripts
- [Opencv] - Open Computer Vision Library
- [cvzone] - opncv optimized library
- [pyautogui]

And of course Cam Utils itself is open source with a [public repository][https://github.com/crs0471/OpenCv]
 on GitHub.

### Installation

Cam Utils requires [Python](https://www.python.org/) v3.8+ to run.

Install the Librarysrun the scripts.

```sh
pip install -r requiremets.txt
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```

## Control Window Using Hands

this script will control window , switch between opened application or windows using hand gasture.

### How To Use

```sh
cd control_with_hand
python main.py
```
![Hand Landmarks](https://developers.google.com/static/mediapipe/images/solutions/hand-landmarks.png)
please refer [https://developers.google.com/mediapipe] for more details

#### Change Action modes
put two hand infront of camera and close first hand palm to change actions
there are 3 actions:
- None
- Volume (controle volume)
- Windows (controle windows and opened applications)

you can watch active action on top left corner of cam stream

#### change volume
while active action is **Volume** :
- put point 4 and 8 closer to lower the volume 
- put point 4 and 8 away to increase the volume

#### control window and open applications
while active action is **Windows** :
- put point 4 and 8 closer to toggle switch mode 
- put point 4 and 12 closer to switch between application switch mode, windows switch mode or window add mode (Tab key).
- put point 4 and 16 closer to go to next window/application (Left Key)
- put point 4 and 13 closer to select (Enter Key)


## Drag And Drop Using Hand

Whit this script user can create rectangle object on camera stream window , drag it to anyware, delete it.

### How To Use

```sh
cd drag_drop_with_hand
python main.py
```
please refer **hand lendmark image** above or [https://developers.google.com/mediapipe] for more details

#### Add rectangle
- put point 4 and 8 closer

#### hold ,drag and drop rectangle
- put point 12 and 8 closer while hand point 8 is in rectangle to hold rectangle
- while putting point 12 and 8 closer move hand ponit 8 to anyware to drag rectangle
- put point 12 and 8 away to drop rectangle

drop rectangle inside red trash area to delete reactangle



