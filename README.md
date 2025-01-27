# hoyo-redeem-codes

python project to be used for my own personal use to notify me (or redeem?) of new genshin redeem codes


## requirements

python `3.11.2` and above. will be used to my own debian 12 instance or github actions


## usage

```bash
# if you have pyenv, use python 3.11.2

# activate venv
# then install reqs
pip install -r requirements.txt

# setup .env
cp .env.example .env

python main.py

# or this if you just want dummy data to test if it works
python main.py literally any text here
```