## Spot Nuclei. Speed Cures.

We’ve all seen people suffer from diseases like cancer, heart disease, chronic obstructive pulmonary disease, Alzheimer’s, and diabetes. Many have seen their loved ones pass away. Think how many lives would be transformed if cures came faster.

Identifying the cells’ nuclei is the starting point for most analyses because most of the human body’s 30 trillion cells contain a nucleus full of DNA, the genetic code that programs each cell. 

Nuclei identification is a pivotal first step in many areas of biomedical research. Pathologists often observe images containing microscopic nuclei as part of their day-to-day jobs. 

During the research, pathologists must identify nuclei characteristics from microscopic images such as volume of nuclei, size, density, and individual position within the image. 

Identifying nuclei allows researchers to identify each individual cell in a sample, and by measuring how cells react to various treatments, the researcher can understand the underlying biological processes at work.

### Technologies Used -
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Firebase](https://img.shields.io/badge/Firebase-039BE5?style=for-the-badge&logo=Firebase&logoColor=white)

<details open>
<summary>Install</summary>

```bash
git clone https://github.com/AvyaRathod/Project-NS  # clone
pip install -r requirements.txt  # install
```

</details>
<details open>
<summary>Model</summary>

Developed multiple versions of U-Net implementation as proposed by [Ronneberger et al.](https://arxiv.org/pdf/1505.04597.pdf) using Tensorflow 2 over the [Data Science Bowl 2018](https://www.kaggle.com/competitions/data-science-bowl-2018/data) dataset

#### Models developed:

- [Unet Model](https://github.com/AvyaRathod/Project-NS/blob/main/model_training/UNET%20BASE.ipynb)
- [Attention Unet Model](https://github.com/AvyaRathod/Project-NS/blob/main/model_training/ATTENTION-UNET.ipynb)
- [Attention Residual Unet Model](https://github.com/AvyaRathod/Project-NS/blob/main/model_training/ATTENTION-RES-UNET.ipynb)

You can download the trained model files from [here](https://drive.google.com/drive/folders/1d3o5Kt6mTavuedE8oHzvYfA4MWCQLl-k?usp=sharing).

To use the model use:

```bash
from unet_models import jacard_coef, jacard_coef_loss
model = load_model('unet_test.h5', custom_objects={'jacard_coef': jacard_coef})
```


#### Training curves:
![image](https://user-images.githubusercontent.com/27121364/198712608-0dc6912b-6aaf-48a0-aac3-ef6fd02ab576.png)

| Model  | Accuracy | IOU(Jaccard) |
| ------------- | ------------- | ------------ |
| Unet Model  | 96.47%  | 0.8038 |
| Attention Unet Model  | Yet to be trained | Yet to be trained|
| Attention Residual Unet Model | 96.86% | 0.8186 |

Outputs:
![image](https://user-images.githubusercontent.com/27121364/198721762-feb98315-320b-4bd6-b457-276aaa4fde0e.png)
</details>

<details open>
  <summary>Workflow</summary>
To provide a seamless experience to the user a dashboard is created, integrated with a terminal application which shows the live stream with the segmented nuclei and a nuclei count, and allows the user to save an instance of the stream to the database which can be accessed from the frontend.
  
![image](https://user-images.githubusercontent.com/27121364/198722347-6ad459be-29ef-4837-8d5e-97fc989b9a4f.png)
</details>

## Authors -
<div align="left"> 
  <table>
  <tr align="left">
   <td>

   #### Avya Rathod
   <p align="center">
   <img src = "https://avatars.githubusercontent.com/u/27121364?s=400&u=263e4e69519c05c350b874efc6120f411d130a67&v=4"  height="120" alt="Avya Rathod">
   </p>
   <p align="center">
   <a href = "https://github.com/AvyaRathod"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
   <a href = "https://www.linkedin.com/in/avya-rathod-38b635225/">
   <img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
   </a>
   </p>
    <strong>ML and CV Developer<strong>
    </td>
    <td>

   #### Riya Batla
   <p align="center">
   <img src = "https://media-exp1.licdn.com/dms/image/C4D03AQF9sqBsGQ4Ixw/profile-displayphoto-shrink_400_400/0/1644657834803?e=1672272000&v=beta&t=bOGup9psS0730vR7yHXAkxbp7M6WVz6dlcxLUXhcsxU"  height="120" alt="Riya Batla">
   </p>
   <p align="center">
   <a href = "https://github.com/cereal-hecker"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
   <a href = "https://www.linkedin.com/in/riya-batla/">
   <img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
   </a>
   </p>
    <strong>Frontend Developer<strong>
    </td>
<td>

#### Nikhil I
<p align="center">
<img src = "https://media-exp1.licdn.com/dms/image/C4E03AQEsJd7i6LPYVQ/profile-displayphoto-shrink_400_400/0/1643037859646?e=1667433600&v=beta&t=AzSjF6UkmGr3hH2vlP4e3S6mHqbk4_jKPpqkDtnb2gE"  height="120" alt="Aryan Raj">
</p>
<p align="center">
<a href = "https://github.com/ironnicko"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/nikhil-ivannan-351036201/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
 <strong>Competetive Programmer<strong>
</td>

