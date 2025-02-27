# Calculate Your Score!! :dizzy_face:

  - [Introduction! :heartbeat:](#introduction-heartbeat)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Start](#start)
  - [Other](#Other)

## Introduction! :heartbeat:
This project is simply for *calculating your score*
~~You don't need to worry about your privacy.~~ The entire program is deployed locally, so there are absolutely no concerns.

## Features
- **Score Calculation**: Automatically calculates the weighted average score based on the input data.
- **Data Analysis**: Provides detailed analysis and visualization of the scores.
- **User-Friendly Interface**: Easy-to-use graphical interface for inputting data and viewing results.


## Dependencies
- **environment.yml**: Contains the environment configuration and dependencies for the project.
- **requirements.txt**: Lists additional Python packages required for the project. 

## Start
First, navigate to the project directory:
```bash
cd path/to/project
```

Create a new Conda environment using the `environment.yml` file and activate it:
```bash
conda create --name <your_env_name> --file environment.yml
conda activate <your_env_name>
```

Install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

Finally, run the main script. After running the script, the application will start a local server. Enter the URL and ~~enjoy it~~ calculating your score!
```bash
python main.py
```
## Other
- The excel file `course.xlsx` is used to store the course information and it is the default data of the program.
- You can modify `config.json` to modify some details of the program. 
- `experiment.py` is used for a quick start and also for debugging.
- If you are willing, you can package this project into a software as a contribution, and we will be extremely grateful.




