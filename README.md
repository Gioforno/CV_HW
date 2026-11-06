# HOW EXECUTE THE HOMEWORK

## Prerequisites

- All libraries used in this implementation are in requirements.txt
- develped on Fedora 43 with pyhton 3.14.7

## configure virtual environement

To create and work inside the virtual environement for this project, is necessary to run this commands (tested on Fedora 43, on other OS the commands may differ a bit)

```bash
python -m venv hw1env #create venv
source hw1env/bin/activate #activate venv
python -m pip install -r requirements.txt #install necessary libraries
```

## real execution

Run `python main.py` to start the execution.

All output image will be written on `output_img/`. After the first execution, the output photos will be overwritten every exectuion: if you change some parameters and want to keep some previous processed images, change their name or bring them outside the `output_img/` folder.
