## cranehook
cranehook is a small webhook API application run specified command when webhook called from GitHub.
It's designed to use with pelican generated website and also capable to run other tasks you need.

## Status
It's in alpha state. We've just start using this program.

Only `ping` and `pullrequest` event are handled. (Even `pullrequest` handling is limited.)

### ping event
Just response `pong`.

### pullrequest event
When event is `pullrequest` and its payload have `merged` property as `True`, cranehook runs commands written on `settings.py`.

## Usage
At first, do `git clone git@github.com:sonkm3/cranehook.git` to get a copy of cranehook.

Install required python modules `pip install -r requirements.txt`

Update `settings.py` as you need.

Run as web server. `python cranehook.py`

Webhook is waiting on this url. `http://localhost:8080/` (Port can be changed by editing `settings.py`)


## Test
Just run `nosetests`

## Background
I and friends are making a Podcast since 2021/01. To generate website, we use pelican and GitHub to generate and manage contents, use self-hosted container due to deliver large size audio file. Because we self-host static file host server, we need some work to make it automatically updated. That's why this small program made, and that's why this program called crane hook. (At first Pelican hook came out as a name, but its usage seems much more generic, so we choose crane for name, it's kind of a bird as Pelican.)

