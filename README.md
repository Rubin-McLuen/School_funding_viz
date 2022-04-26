# Simple Dash App Template
This was constructed as a simple dash app template.  The basic instructions for getting it setup on Google Cloud are below (but not required for the assignment).

## Basic Usage instructions

If you are just wanting to run the app locally, you can do so by navigating to the directory and running the main application (myapp.py) with Python:

```bash
python myapp.py
```

The app should indicate that it is now running and accessible at the following URL: localhost:8080

The local environment can be stopped by pressing Ctrl-C in the terminal, or by stopping the app in the browswer.

## Google App Engine Instructions

Google App Engine is an easy, fully managed option for deploying web applications.  The dash app itself can be loaded into App Engine and given a URL of it’s own.  The service is NOT free, but low usage is provided at no cost with hard thresholds able to be set.

Detailed instructions can be found [here](https://www.phillipsj.net/posts/deploying-dash-to-google-app-).

## Google Virtual Machine Instructions



Sometimes a fully managed solution is not desired and instead we want to host our own.  The following instructions are for those individuals who want to use a dash application on their own self-managed device.  Here I will assume you have a fresh install of Ubuntu 20.04 LTS.

Note, this should NOT be done on your own personal machine.  A cloud virtual machine that is properly firewalled is best.

1. Create a fresh server.  If using Google Cloud, I recommend something small like: N1 type, f1 micro instance
2. Install the following using `apt`: 
```bash
sudo apt install python3-pip build-essential nginx
```

3. Install the following with `pip`: 
```bash
sudo pip install dash uwsgi numpy pandas
```
4. Git clone this repository onto the server
5. Test out with `python3 myapp.py`.  Should see the stanard debug web server for Dash.
6. Make the `wsgi.py` file inside app directory with the following contents:
```bash
from myapp import server as application
if __name__ == '__main__':
    application.run()
```

7. Make the `startup.ini` file inside the app directory with the following contents:
```bash
[uwsgi]
module = wsgi:application
master = true
processes = 5
socket = index.sock
chmod-socket = 664
vacuum = true
die-on-term = true
logto=/var/log/wsgi.log
```

Test out with: `uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi`.  There should not be any errors.

8. Make `dash_app_startup.service` file in `/etc/systemd/system/` with the following contents:
```bash
[Unit]
Description=uWSGI instance to serve startup
After=network.target

[Service]
User=mstobb
Group=www-data
WorkingDirectory=/home/mstobb/dash_app_template
ExecStart=uwsgi --force-cwd /home/mstobb/dash_app_template --ini startup.ini

[Install]
WantedBy = multi-user.target
```
Be sure to replace the username with YOUR username.

9. Start the process: 

    1. To start: `sudo systemctl restart dash_app_startup.service`

    2. To check: `sudo systemctl status dash_app_startup.service`

10. Make reverse proxy file `dash_app` in `/etc/nginx/sites-available/` with the following contents:
```bash
server {
    listen 80;

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/home/mstobb/dash_app_template/index.sock;
    }
}
```
Again, be sure to change the username to YOUR username.

11. Copy the reverse proxy file to `sites-enabled`: 
```bash
sudo ln -s /etc/nginx/sites-available/dash_app /etc/nginx/sites-enabled
```

12. Remove default proxy setting in `/etc/nginx/sites-enabled`:
```bash
sudo rm /etc/nginx/sites-enabled/default
```

13. Activate the proxy:

    1. To start: `sudo service nginx restart`

    2. To check: `sudo service nginx status`

14. Visit IP address - your app should be visible!

