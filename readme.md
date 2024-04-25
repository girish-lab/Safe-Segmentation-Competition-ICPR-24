
<h1 align="center">
    <a href="https://github.com/girish-lab/Safe-Segmentation-Competition-ICPR-24"> ICPR 2024 Competition on Safe Segmentation of Drive Scenes in  Unstructured Traffic and Adverse Weather Conditions</a>
</h1>
<p align="center"> <a  href="https://girish-lab.github.io/Safe-Segmentation-Competition-ICPR-24/">Home</a>  <a  href="http://yourdomain.com/about">Overview</a> <a href="https://iddaw.github.io/">Dataset</a> <a href="http://yourdomain.com/contact">Instructions </a> </p>

<p align="center">
This is a competition running for several months aimed at assessing the performance of semantic segmentation models in adverse weather conditions for autonomous driving. Participants are provided with the IDD-AW dataset, comprising 5000 pairs of high-quality images with pixel-level annotations, captured under adverse weather conditions such as rain, fog, low light, and snow.
</p>
    
<h2 align="center">Updates & News</h2>

   Registration Start
    
<h2 align="center"> Registration </h2>
1. Click to [Download here] button below in the Dataset details. This will redirect you to the registration page.
1. Register an account at http://idd.insaan.iiit.ac.in/.
2. Go to Dataset > Download page in the menu.
3. Download the IDD-AW Dataset  by clicking on 'Download' under 'IDD AW Dataset'. This will generate a 24 hour token to download the dataset.
4. Extract the downloaded compressed file into a folder.
5. Please run the data preparation code for generating ground truth segmentation masks as documented here: https://github.com/AutoNUE/public-code. Use the following command for segmentation mask generation:
python preperation/createLabels.py --datadir $ANUE --id-type level3Id --num-workers $C 

<h2 align="center"> Objective </h2>

<p align="center">
The central challenge addressed by the competition is optimizing the Safe mIoU metric for semantic segmentation in adverse weather conditions to ensure the safety of autonomous driving systems. Semantic segmentation plays a pivotal role in enabling autonomous vehicles to understand their surroundings, but adverse weather conditions pose significant challenges, often leading to hazardous situations. The competition aims to develop robust models that accurately segment driving scenes even in adverse weather conditions, focusing on prioritizing safety-related mispredictions.
</p>

<h2 align="center"> Timeline </h2>

| Deadline    | Date |
| -------- | ------- |
| Registration    | July 21, 2024 |
| Competition Report Submission  | August 18, 2024    |
| Camera-Ready Papers | September 02, 2024     |
| Communicate Winners to Chairs    | October 28, 2024    |
| Presentation at ICPR Conference | December 1-5, 2024 |


<h2 align="center"> Guidelines </h2>

<h2 align="center"> Awards </h2>

    1 
    2
    3



<h2 align="center"> Dataset details </h2>



<p align="center">
The dataset consists of images collected in an unstructured road scenario, driving in adverse weather conditions of rain, fog, lowlight and snow. Each individual RGB image has a more detailed near-infrared image (NIR) captured simultaneously. The images are collected using JAI FS-3200D-10GE camera.
</p>


<a align="center" href="https://iddaw.github.io/"> Dataset page</a>

<a align="center" href="https://idd.insaan.iiit.ac.in/dataset/download/">Download here</a>

<p align="center">
The dataset, including training data, ground truth, and an evaluation script, will be made publicly available post-competition in accordance with ICPR guidelines.
</p>

<h2 align="center"> Methods: </h2>


<h2 align="center"> Evaluation Metrics: </h2>

[code](https://github.com/Furqan7007/IDDAW_kit)

    1 Safe mIoU
    2 ...
    3. code [link]([https:](https://github.com/Furqan7007/IDDAW_kit))

<h2 align="center"> Leaderboard </h2>


<h2 align="center"> Organisers </h2>

![alt text](/assest/drirish.png) ![alt text](/assest/furqan.png) ![alt text](assest/sandeep.png)


Dr Girish Varma, C-STAR and ML Lab at IIIT Hyderabad

Furqan Ahmed, ML Lab, IIIT-Hyderabad

Sandeep Nagar, ML Lab, IIIT-Hyderabad





<h2 align="center"> Reference </h2>

[https://iddaw.github.io/](https://iddaw.github.io/)

Furqan Ahmed Shaik, Abhishek Reddy, Nikhil Reddy Billa, Kunal Chaudhary, Sunny Manchanda, Girish Varma; Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), 2024, pp. 4614-4623

<h2 align="center">
    FAQ:
</h2>

    1
    2
    3
    4
    5
    6
    

<h2 align="center">
    Contacts:
</h2>
If you have any question regarding to this Competition, please send an email to the following address:

furqan.shaik@research.iiit.ac.in or sandeep.nagar@research.iiit.ac.in

Furqan Ahmed

[Sandeep Nagar](https://twitter.com/NaagarRN)

[girish-lab](https://girishvarma.in/)

