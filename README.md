# Team Snorlax - Term Project for Technology for Special Needs Education (ET60029) Spring 2021 

### Team members:

Nikhil Shah - 17CS10030   
Apoorve Singhal - 17CS30007   
Sombit Dey - 17EC10056  
Harsh Sah - 17EE10014   
Arvind Jha - 17MT10009  

### Overview of the project
The objective is to design a portable and affordable app, to help **visually impaired individuals** to assist them in traveling around and provide information about their surroundings. 

### Demo of the app: 
https://www.youtube.com/watch?v=dFS_E4YjFGA

### How to use the App
Here are the elements of the app:
- Restart Button: To restart the app. It basically erases all the temporary variables stored in the memory
- Switch Cam Button: To switch from one video-feed to another. The video feeds available in this prototype apps are web-cam, a pre-recorded video and mobile camera(using IP webcam app)
- Capture button: To start the Visual Question Answering. When pressed, the app stores the image and records a question, and then sends these to the VQA model and the answer returned is displayed in the screen as well as converted to speech and spoken out.
- Messsage Display area: Where the answers and questions are displayed
- Video Screen: Where the video feeds are displayed

### Flow of the app
The app is made of python, using kivy for user-interface; and mainly pytorch and numpy as the backend. The model described above uses pytorch, numpy, seaborn, matplotlib, gdown, opencv_python and their dependencies.
![image1](https://user-images.githubusercontent.com/39180194/115139560-17ad6700-a050-11eb-86e0-ba2a01fbb3c3.png)

### Working of the VQA Model
We have implemented Visual Question Answering Model proposed by [Multi-modal Factorized Bilinear Pooling with Co-Attention Learning for Visual Question Answering](https://arxiv.org/abs/1708.01471).
The model takes an image and a question string as inputs and outputs an answer string.

### Future improvements
One can add modules to the app so that all the functions mentioned above are voice activated or be coupled to some external hard buttons. 


