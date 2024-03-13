![](static/img/logo.jpg)

### CREDO image search engine

Flask implementation of algorithm:

Piekarczyk, M.; Hachaj, T. On the Search for Potentially Anomalous Traces of Cosmic Ray Particles in Images Acquired by Cmos Detectors for a Continuous Stream of Emerging Observational Data. Sensors 2024, 24, 1835. https://doi.org/10.3390/s24061835 

Entry points are in file [test.py](test.py)

## Setup

1 Download embedding [embedding.npy (2714MB)](https://drive.google.com/file/d/1FVGa3gGYjr_Mx2o_nibBr9bgU_ZIizQV/view?usp=sharing) and put in in the [data](data/) folder 

2 Download CREDO dataset [CREDO dataset (1014MB)](https://drive.google.com/file/d/1jSuQXfxFzWsFoTEYDno1V_Aqn5AaNs_I/view) and set path to  in file [test.py](test.py) by assigning variable:

```
path_to_data = 'd:/Folder_with_credo_dataset'
```

## Using the app

1 Open website in browser, select a \*.png file (query image) with hit data, select number of similar images to find and click Search button.

![](img/index.jpg)

2 You should be redirected to website that shows most similar images and distance in embedding space between query image and results. You can return to previous page by clicking Next search button.

![](img/images.jpg)

![](static/img/logo.jpg)