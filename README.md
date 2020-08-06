# GDPR Bot


## Local Set-up

The instructions down below will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to install Python and the package manager PIP. When you install Python <= 3.4 from the [official website](https://www.python.org/downloads/), PIP is already installed.

Rasa needs either Python 3.6 or 3.7.

To check your Python Version, enter the following command in your console/terminal.

```bash
# Install virtual enviroment
python3 --version
```
If the version number starts with 3.6 or 3.7, you can continue with the [the installation here](#Python-36-amp-37).

If you get an error saying "python3: command not found", please install Python 3.7.8 from [here](https://www.python.org/downloads/release/python-378/) and with the [the installation here](#Python-36-amp-37).

If you get a different version number, you need to follow the instructions for pyenv-virtualenv [here](#other-python-versions)

## Python 3.6 & 3.7

```bash
# Install virtual enviroment
pip install virtualenv
```

First set-up and start the virtual environment.

```bash
# Create virtualenv
virtualenv -p python3 bot

# Start environment
source bot/bin/activate

```

## Other Python versions

Take a look at the [official documentation](https://github.com/pyenv/pyenv-virtualenv) for more information regarding the installation of pyenv-virtualenv.

1. Check out pyenv-virtualenv into plugin directory.

```sh $ git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv ```

2. Add `pyenv virtualenv-init` to your console/terminal to enable auto-activation of virtualenvs. This is entirely optional but pretty useful. See "Activate virtualenv" below. ```sh $ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
 ```

Next, run the following commands. It will download the Python version we want to use and set up a virtual environment.

```bash
pyenv install 3.7.8
pyenv virtualenv 3.7.8 bot
```

Start the virtual environment using

```bash
pyenv activate bot
```
Now, continue with the next section.

## Clone and install the project

Now clone the repo to the "src"-folder or download the [repo](https://github.com/fbennets/HCLC-GDPR-Bot) as zip, unpack the folder, move it into the folder of your environment and rename it to "src".

```bash
# Clone repository to current directory
cd bot
git clone https://github.com/fbennets/HCLC-GDPR-Bot src

```
Next install the requirements. If you get to many dependency errors, try to use the second command.

```bash
# Install dependencies
cd src
pip install -r requirements.txt

OR

pip install rasa[spacy]
```

Now, get the models for spacy to do the language processing.
```bash
python -m spacy download de_core_news_md
python -m spacy link de_core_news_md de
```

Train the language model and run the tests.
```bash
rasa train
rasa test
```

You're ready to start a conversation with your bot!
```bash
rasa shell
```

## Built With

* [Rasa](https://rasa.com/) - The Rasa bot-framework used

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/fbennets/HCLC-GDPR-Bot/blob/master/LICENSE) file for details.

## Links

* [HCLC Website](https://hclc-berlin.de/)
