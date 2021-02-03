## cranehook
cranehook is a small webhook API application run specified command when webhook called from github.
It's designed to use with pelican generated web site and also capable to run other tasks you need.

## Status
It's in alpha state. We've just start using this program.

## Usage
At first, do `git clone` to get a copy of cranehook.

Install required python modules `pip install -r requirements.txt`

Update `settings.py` as you need.

Run as web server. `python cranehook.py`

Webhook is waiting on this url. `http://localhost:8080/` (Port can be changed by editing `settings.py`)

Only `ping` and `pullrequest` event are handled. (Even `pullrequest` handling is limited.)

## Test
Just run `nosetests`

## Background
Me and friends are making a Podcast since 2021/01. To generate web site, we use pelican and github to generate and manage contents, use self hosted container due to deliver large size audio file. Because we self host containts server, we need some work to make it automaticaly updated. That's why this small program made, and that's why this program called crane hook. (At first Pelican hook came out as a name, but it usage seems much more generic, so we choose crane for name, it's kind a bird as Pelican.)

