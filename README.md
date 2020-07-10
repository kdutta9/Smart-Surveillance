# Smart Security Camera
An Internet of things security camera that notifies users via SMS, WhatsApp, 
and/or shared network folder when it detects motion, powered by Raspberry Pi, Amazon Web Services (AWS), and Twilio.

![Display](https://i.imgur.com/o6gIMUo.png)

See my [blog post about this project](https://kdutta9.github.io/projects/2020/07/07/Smart-Surveillance/).

## 📝 Table of Contents
- [Getting Started](#getting_started)
- [Software Used](#software)
- [Contributing](./CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Build Kit
- Raspberry Pi
	- I used a Raspberry Pi Zero W.
- Camera
	- I used the [Raspberry Pi Camera Module V2](https://www.raspberrypi.org/products/camera-module-v2/).
		
### Prerequisites
This project is built in Python 3, so use pip3 to install packages using bash:

```bash
sudo apt install python3-pip
```

To enable support for messaging, AWS S3 and Twilio (or a similar cloud storage platform and messaging API, respectively) are needed.

Refer to the [AWS guide for S3](https://docs.aws.amazon.com/AmazonS3/latest/dev/Introduction.html), for a guide on how to use S3 to store the media files.

Refer to the [https://www.twilio.com/docs/iam/api](Twilio documentation), for a guide on how to use the Twilio API to send messages.

To enable sharing on a network folder, refer to the [https://websiteforstudents.com/mount-windows-10-share-on-ubuntu-18-04-16-04/](Ubuntu mounting walkthrough), for a guide on how to mount a shared folder on a Raspberry Pi.


### Installing
Clone the repository by running:
```bash
git clone https://github.com/kdutta9/Smart-Surveillance.git
```
I recommend using a virtual environment, using <i>virtualenv</i>, for the project, to ensure there are no errors with dependencies. Make sure you create in the virtual environment in the project directory.
- Installing virtualenv
	```bash
	sudo pip3 install virtualenv
	```
- Creating a virtual environment of some name (i.e. venv)
	```bash
	cd Smart-Surveillance
	virtualenv venv
	```
- Activating virtual environment
	```bash
	source venv/bin/activate
	```

Then, install the required packages.
```bash
pip3 install -r requirements.txt
```

If needed, modify <i>config.json</i> with your API keys and then use the following to run the application:
```bash
python3 main.py
```

If you need to run the application as the root user, modify and execute the script <i>run.sh</i> as such:
```bash
./run.sh
```

## Software Used <a name = "software"></a>
- [Python](https://www.python.org/)
- [OpenCV](https://opencv.org/) - Object Detection
- [ImUtils](https://github.com/jrosebr1/imutils/) - Image Processing
- [Amazon Web Services](https://aws.amazon.com/) - Cloud Storage
- [Twilio](https://www.twilio.com/docs) - Messaging API 

## Authors <a name = "authors"></a>
- [@kdutta9](https://github.com/kdutta9)
- [Adrian Rosebrock](https://github.com/jrosebr1): I used Adrian's guide to motion detection and use of the Twilio API, linked in Acknowledgements, to guide my project.

See also the list of [contributors](https://github.com/kdutta9/Smart-Surveillance/graphs/contributors) who participated in this project.

## Acknowledgements <a name = "acknowledgement"></a>
- Inspiration for using the Twilio API: [Adrian Rosebrock](https://www.pyimagesearch.com/2019/03/25/building-a-raspberry-pi-security-camera-with-opencv/)
- Inspiration for motion detection: [Adrian Rosebrock](https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/)
- Inspiration for using a network folder: [Website for Students](https://websiteforstudents.com/mount-windows-10-share-on-ubuntu-18-04-16-04/)
