# AutoAttend
AISG Student Hackathon 2021 - AutoAttend Submission


## Overview
AutoAttend is a submission for the AISG Student Hackathon 2021, and it uses the AISG [PeekingDuck](https://github.com/aimakerspace/PeekingDuck) CV brick. The idea of this project is to have a teacher submit a picture of the classroom. The system will then recognise the face and then record down their presence in the classroom in a MongoDB database.

## Features
### Attendance Taking using Photo and Face Recognition
The main feature of this system is that it uses Face Recognition to do the attendance taking. So, instead of manually recording each person's attendance or having your student mark their own attendance, the teacher just has to take a photo to do the attendance taking. This makes it faster, and it reduces the need for physical contact as well, which is important, especially with the still ongoing pandemic situation.

## Improvements available
### Reliance on Azure
Currently, the face recognition is done using Microsoft Azure's [Face API](https://azure.microsoft.com/en-us/services/cognitive-services/face/). Even though that might make life way easier, there is a limit to the number of transactions available per minute, or at least of the Free Instance (20 transactions per minute). Another downside will be that if the API was to ever be down, the whole system would not work.
A possible solution would be to do a transfer learning on face recognition models such as FaceNet or VGG16.

### There is only one Person Group
A person group is basically a container of the person data for the Azure Face API, in which so far for this project, there is only one. A possible improvement that can be done would be to create multiple person groups, each for each class.
