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

## execution&output

Run `python main.py` to start the execution.

All the results of the implementation will be written inside `output/`:

- metrics will be in `output/mtrics.csv`
- images will be in `output/output_img/`. Please note that each execution overwrite images in this folder. if you want to keep some previous processed images before the execution change their name or bring it outside the folder
