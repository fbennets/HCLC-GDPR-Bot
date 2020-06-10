# GDPR Bot


## Local Set-up

The instructions down below will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to install Python and the package manager PIP. When you install Python <= 3.4 from the [official website](https://www.python.org/downloads/), PIP is already installed.

```bash
# Install virtual enviroment
pip install virtualenv
```

### Installation

First set-up and start the virtual environment.

```bash
# Create virtualenv
virtualenv -p python3 bot

# Start environment
source od/bin/activate

```

Now clone the repo to the "src"-folder or download the [repo](https://github.com/fbennets/HCLC-GDPR-Bot) as zip, unpack the folder, move it into the folder of your environment and rename it to "src".

```bash
# Clone repository to current directory
cd bot
git clone https://github.com/fbennets/HCLC-GDPR-Bot src

```
Next install the requirements.

```bash
# Install dependencies
cd src
pip install -r requirements.txt
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
