# HOW EXECUTE THE HOMEWORK

## Prerequisites

- All libraries present in requirements.txt
- pyhton 3.14.7 (tested, other version not guaranteed)

## configure virtual environement

To create and work inside the virtual environement for this project, is necessary to run this commands

```bash
python -m venv hw1env #create venv
source hw1env/bin/activate #activate venv
python -m pip install -r requirements.txt #install necessary lib
```

## real execution

Run `python main.py` to start the execution

All output image will be written on `output_img/`. After the first execution, the photo will be overwritten due to having the same name: if you change some parameters and want to keep some previous processed images, change their name or bring them outside the output folder.
