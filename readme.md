
# Safe-Segmentation-Competition-ICPR-24

## Leaderboard: [Codalab](https://codalab.lisn.upsaclay.fr/competitions/18745)
## Test dataset from [OneDrive](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/sandeep_nagar_research_iiit_ac_in/Ef7Qu783hx9ItwJN-5Cd_HYBGWmwdzyQ5onzQFLpbp-pcQ?e=d4j7XS)
## Test dataset released here: [download form here](https://datafoundation.iiit.ac.in/city-scale-road-audit)
    steps: 
        1. Sign up here: https://datafoundation.iiit.ac.in/sign-up
        2. Login and search 'IDDAW Safe Segmentation Test Dataset', here: https://datafoundation.iiit.ac.in/city-scale-road-audit
        3. Click download, and you can generate the labels for them.
        
## <a  href="https://girish-lab.github.io//">Home</a> <br> <a  href="https://girish-lab.github.io/Safe-Segmentation-Competition-ICPR-24/">Overview</a> <br> <a href="https://iddaw.github.io/">Dataset</a> <br> <a href="https://girish-lab.github.io/Safe-Segmentation-Competition-ICPR-24/">Instructions </a> 

Semantic segmentation plays a pivotal role in enabling autonomous vehicles to understand their surroundings, but adverse weather conditions pose significant challenges, often leading to hazardous situations. The central challenge addressed by the competition is optimizing the Safe mIoU metric for semantic segmentation in adverse weather conditions to ensure the safety of autonomous driving systems.

This competition is aimed at assessing the performance of semantic segmentation models in adverse weather conditions for autonomous driving. Participants are provided with the IDD-AW dataset, comprising 5000 pairs of high-quality images with pixel-level annotations, captured under adverse weather conditions such as rain, fog, low light, and snow. Emphasizing correctly identifying safety-critical elements and penalizing unsafe false predictions (False). The Participants aim to develop robust models that accurately segment driving scenes even in adverse weather conditions, focusing on prioritizing safety-related mispredictions.

## To register: [Fill this form](https://forms.office.com/r/61Xu4QDTQK)

## Sample dataset: https://drive.google.com/drive/folders/1YZMmtf-HHH_XYFrBQy0pk9HaBkwalYgp



## Guidelines 

#### How to Participate 

Before you can submit your first results, you need to register with CodaLab and log in to participate. Only then can you submit results to the evaluation server, which will score your submission on the non-public test set. 

    Steps:
        1. Prepare your submission in the required format, as described under the Evaluation section. CodeLab expects you to upload a single zip.
        2. Use the validation script from the code repo to ensure that the folder structure and number of label files in the zip file are correct. All submissions count towards the overall maximum number of submissions!
        3. Go to Participate and the Submit / View Results page.
        4. Select the appropriate phase, i.e., Single Scan or Multiple Scan, for which you computed the results.
        5. Enter the required fields, where you can also supply more details later if you need to take care of anonymity in case of double-blind submissions.
        6. Then, you have to click "Submit" in the lower part of the page, which will open a file dialogue. In the file dialogue, you have to select your submission zip file, which will then be uploaded.
        
        - The evaluation takes roughly 10 minutes to complete, and you will have the choice of which of your submissions gets added to the leaderboard.

Good luck with your submission!

Submission Policy: Only the training set is provided for learning the parameters of the algorithms. The test set should be used only for reporting the final results compared to other approaches - it must not be used in any way to train or tune systems, for example, by evaluating multiple parameters or feature choices and reporting the best results obtained. Thus, we impose an upper limit (currently 5 attempts) on the number of submissions. It is the participant's responsibility to divide the training set into proper training and validation splits, e.g., we use sequence 08 for validation. The tuned algorithms should then be run - ideally - only once on the test data and the results of the test set should not be used to adapt the approach. 

We ask each participant to upload the final results of their algorithm/paper submission only once to the server and perform all other experiments on the validation set. If participants would like to report results in their papers for multiple versions of their algorithm (e.g., parameters or features), this must be done on the validation data, and only the best-performing setting of the novel method may be submitted for evaluation to our server. If comparisons to baselines from third parties (not evaluated on the benchmark website) are desired, please contact us for a discussion. 



## Dataset details

The dataset consists of images collected in an unstructured road scenario, driving in adverse weather conditions of rain, fog, low light and snow. Each individual RGB image has a more detailed near-infrared image (NIR) captured simultaneously. The images are collected using a JAI FS-3200D-10GE camera.
The dataset comprises 5000 images, manually selected to represent various adverse weather scenarios, including rain, fog, low light, and snow. Each RGB image also has a paired NIR image to provide image enhancement. Each image is densely annotated at the pixel level for semantic segmentation, utilizing a label set with a hierarchical structure consisting of 7 labels at level 1 and 30 labels at level 4.


<a align="center" href="https://iddaw.github.io/"> Dataset page</a>

<a align="center" href="https://idd.insaan.iiit.ac.in/dataset/download/">Download here</a>

## Dataset Download  

        1. Click to <a href="https://idd.insaan.iiit.ac.in/dataset/download/">download</a> the Dataset and more details. This will redirect you to the registration page to download the dataset.
        2. Register an account at http://idd.insaan.iiit.ac.in/.
        3. Go to Dataset > Download page in the menu.
        4. Download the IDD-AW Dataset  by clicking on 'Download' under 'IDD AW Dataset'. This will generate a 24 hour token to download the dataset.
        5. Extract the downloaded compressed file into a folder.
        6. Please run the data preparation code for generating ground truth segmentation masks as documented here: https://github.com/AutoNUE/public-code. Use the following command for segmentation mask generation:
        run $ `python preperation/createLabels.py --datadir $ANUE --id-type level3Id --num-workers $C `


The dataset, including training data, ground truth, and an evaluation script, will be made publicly available post-competition in accordance with ICPR guidelines.

#### Evaluation Metrics and base line code: 

[code](https://github.com/Furqan7007/IDDAW_kit)

    1 Safe mIoU
    2 ...
    3. code [link]([https:](https://github.com/Furqan7007/IDDAW_kit))




## Organisers 

<img src="https://www.iiit.ac.in/files/iiit/GirishVerma.jpg" width="235" height="250"> <img src="https://girish-lab.github.io/group/furqanshaik/pic.jpg" width="240" height="250"> <img src="https://girish-lab.github.io/group/sandeepnagar/pic.jpg" width="250" height="250">


<a href="https://girishvarma.in/"> Dr Girish Varma, C-STAR and ML Lab, IIIT-H</a>              

<a href="https://scholar.google.com/citations?user=rzHNVVgAAAAJ&hl=en&oi=ao"> Furqan Ahmed, ML Lab, IIIT-Hyderabad </a>  

<a href="https://researchweb.iiit.ac.in/~sandeep.nagar/"> Sandeep Nagar, ML Lab, IIIT-H </a>



## Reference 

1. [https://iddaw.github.io/](https://iddaw.github.io/)

2. Furqan Ahmed Shaik, Abhishek Reddy, Nikhil Reddy Billa, Kunal Chaudhary, Sunny Manchanda, Girish Varma; Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), 2024, pp. 4614-4623
    

## Contacts:

If you have any question regarding to this Competition, please send an email to the following address:

furqan.shaik@research.iiit.ac.in or sandeep.nagar@research.iiit.ac.in

Furqan Ahmed

[Sandeep Nagar](https://twitter.com/NaagarRN)

[girish-lab](https://girishvarma.in/)

