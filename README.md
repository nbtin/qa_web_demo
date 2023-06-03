# PROJECT

## To-do list:

- [ ] Introduction.
- [ ] Technical Overview.
- [ ] How to Install.
- [ ] Usage.


## How to run the app
### **I. Docker**

```shell
$ docker-compose up -d --build
```

### **II. Others who do not have Docker**
0. **(optional)** I recommend to create a virtual environment by using conda command. Please note that the python version should be greater than or equal to 3.7

```shell
conda create --name <new-name> python=3.8
```

1. To run the app, you need to clone this project and install all the dependencies which are listed in `requirements.txt` by running the command

```shell
git clone https://github.com/nbtin/cinnamon_ai
cd cinnamon_ai
pip install -r requirements.txt
```


**Note:** The first time you run the app, you will need to be patient :smile:. Because the model download process may take 5 ~ 15 minutes depending on your network speed.