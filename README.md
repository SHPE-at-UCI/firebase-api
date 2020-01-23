# SHPE Sign In

We will be using Flasks project tutorial found [here](http://flask.palletsprojects.com/en/1.1.x/tutorial/).

## Installation

#### [Python3](https://www.python.org/downloads/) & [pip](https://pip.pypa.io/en/stable/)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies of the project.

Clone this project.

```bash
$ git clone https://github.com/SHPE-at-UCI/shpesignin.git
$ cd shpesignin
```

Create a virtualenv and activate it:

```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

Or on Windows cmd:

```
$ py -3 -m venv venv
$ venv\Scripts\activate.bat
```

Install Dependencies:

```
$ pip install -e .
```
### Running Flask

For Linux and Mac:

```
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```

For Windows cmd, use set instead of export:

```
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run
```

For Windows PowerShell, use \$env: instead of export:

```
> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
> flask run
```

You’ll see output similar to this:

```
* Serving Flask app "flaskr"
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```

Stop Virtual Environment
```
$ deactivate
```


### Contributing

We use a feature branch workflow.

Step 1: Create a new branch

```
git checkout -b <milestone_milestone#_issue>
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

### Development

Create a pull request(PR) on the master branch.
Once the PR is approved, the owner of the PR merges the pull request into master branch.
In the future we will have continuous deployments. 

## License

[MIT](https://choosealicense.com/licenses/mit/)
