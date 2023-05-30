# PROJECT

## To-do list:

- [ ] Investigate Docker.
- [ ] Apply Docker to project.
- [ ] Create a django server with 1 API calls.
- [ ] Create a front-end web app.
- [ ] Investigate how the front-end request and wait for the Back-end API.
- ...
## How to run the app
 This app was built using [gradio](https://gradio.app/) - an open-source Python library for a quick and easy to use Machine Learning development.

0. **(optional)** I recommend you to create a virtual environment by using conda command. Please note that the python version should be greater than or equal to 3.7

```shell
conda create --name <new-name> python=3.8
```

1. To run the app, you need to clone this project and install all the dependencies which are listed in `requirements.txt` by running the command

```shell
git clone https://github.com/nbtin/cinnamon_ai
cd cinnamon_ai
pip install -r requirements.txt
```

2. At the end of the stage, you just need to run the `app.py` file and [gradio](https://gradio.app/) will do everything for you.

```shell
python app.py
```

**Note:** The first time you run the `app.py` file, you will need to be patient :smile:. Because the model download process may take 5 ~ 15 minutes depending on your network speed.