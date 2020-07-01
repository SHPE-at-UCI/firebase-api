# SHPE at UCI Member Sign In

Run this powerful authentication website on your computer!  

If you have any questions, comments, or concerns regarding this `README.md`, email git admins [tech.shpe.uci@gmail.com](mailto:tech.shpe.uci@gmail.com?subject=[GitHub SHPE-UCI Help]))

## Installation

For this quick setup to work you will need [Python3](https://www.python.org/downloads/) installed on your computer
You will also need [pip](https://pip.pypa.io/en/stable/) (a Python package manager) to install the dependencies of the project.

1 . Clone this project.

```bash
$ git clone https://github.com/SHPE-at-UCI/shpesignin
$ cd shpesignin
```

2 . Create a Python Virtual Environment and Activate It:

|For Windows:                            | For Mac:                      |
|:---------------------------------------|-------------------------------|
|```$ py -3 -m venv venv             ``` | ```$ python3 -m venv venv  ```|
|```$ . venv/Scripts/activate        ``` | ```$ . venv/bin/activate  ``` |

3 . Install Flask:

```$ pip3 install -r requirements.txt``` 

4 . Run Flask 
```
$ ./runapp.sh
```

5 . You should have seen a output similar to this:

```
* Serving Flask app
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```
6 . Now enter ```127.0.0.1:5000``` on your favorite web browser, check out the site! 🤩🤓🌐

7 . To quit the Flask Server from Terminal:

```Ctrl + C```  (Hold down these keys on your keyboard to create KeyBoard kill signal) 

8 . To exit your Py Virtual Env:

```$ deactivate ```

## Contributing

We use a feature branch workflow.

Step 1: Create a new branch

```
git checkout -b <feature_milestone#>
Examples: git checkout -b Login_Feature_1.1
```

Step 2: Update, add, commit, and push changes

```
git status
git add <some-file> or git add .
git commit
```

Step 3: Push feature branch to remote

```
git push -u origin new-feature
Step 4: Create a pull request
```

## Development

Create a pull request(PR) on the master branch.
Once the PR is approved, the owner of the PR merges the pull request into master branch.
In the future we will have continuous deployments.

## shpe.uci.edu (R&D) infrastructure

In order to test out sign-in web-auth features like `login.uci.edu`, your local Flask server needs to be hosted on a
'.uci.edu' domain. However, to run your local server correctly, you will need to modify your machine's `hosts` file
which should be found at: 

|For Windows:                                | For Mac:                      |
|:-------------------------------------------|-------------------------------|
|```C:\Windows\System32\Drivers\etc\hosts``` | ```$ cd ~; open /etc/hosts ```|

    
In the `hosts` file you should see a line `127.0.0.1   localhost` if you add `127.0.0.1    shpe.uci.edu` right below it,
save it changes, rerun `./runapp.sh -h shpe.uci.edu`, now the `login.uci.edu` sign-in should work with no issues. 

## Notes: 
`shpe.uci.edu` can be replaced with something else, but to use UCI cookies `.uci.edu` is needed.

To view a list of changeable parameters for the `./runapp.sh` command:
```
./runapp.sh -?
```

## Tutorial
Watch this [Link](https://www.youtube.com/watch?v=T0Ml5WnQbJY&feature=youtu.be)
Made by Guillermo Hernandez - SHPE Technical Program Manager 2019-2020

This project was kick-started with Flasks project tutorial found [here](http://flask.palletsprojects.com/en/1.1.x/tutorial/).


## License
This official software is held under the [MIT](https://choosealicense.com/licenses/mit/) license
