# RSS- and Atom-Feed Integration Service for Mattermost

This integration service posts RSS feeds into specific Mattermost channels by formatting output from html to text 
via [Mattermost's incoming webhooks](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md).

## Requirements

To run this integration you need:

1. A **network connected device running python** like Raspberry Pi or any other Linux device which supports python and the required packages
2. A **[Mattermost account](http://www.mattermost.org/)** where [incoming webhooks are enabled](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md#enabling-incoming-webhooks)

## Linux/Ubuntu 14.04 Install

The following procedure shows how to install this project on a Linux device running Ubuntu 14.04. 
The following instructions work behind a firewall as long as the device has access to your Mattermost instance. 

To install this project using a Linux-based device, you will need Python 2.7 or a compatible version. 
Other compatible operating systems and Python versions should also work. 

Here's how to start:

1. **Set up your Mattermost instance to receive incoming webhooks**
    1. Log in to your Mattermost account. Click the three dot menu at the top of the left-hand side and go to  
        **Account Settings** > **Integrations** > **Incoming Webhooks**.
    2. Under **Add a new incoming webhook** select the channel in which you want Feed notifications to appear, then click **Add** to create a new entry.
    3. Copy the contents next to **URL** of the new webhook you just created (we'll refer to this as `https://<your-mattermost-webhook-URL>`).

2. **Set up this project to run on your Linux device**
    1. Set up a **Linux Ubuntu 14.04** server either on your own machine or on a hosted service, like AWS.
    2. **SSH** into the machine, or just open your terminal if you're installing locally.
    3. Confirm **Python 2.7** or a compatible version is installed by running:  
        `python --version` If it's not installed you can find it [here](https://www.python.org/downloads/)
    4. Install **pip** and **git**:  
        `sudo apt-get install python-pip supervisor git python-virtualenv`
    5. Clone this GitHub repository:  
        `git clone https://github.com/bitbackofen/Rss-Atom-Feed-Integration-for-Mattermost.git`  
        `cd Rss-Atom-Feed-Integration-for-Mattermost`
    6. Copy sample file `settings.py.sample`:  
        `cp settings.py.sample settings.py`
    7. Edit `settings.py` to suit your requirements:  
        `nano settings.py`  
        Save your changes (F2) and exit nano (CRTL-X)
    8. Setup virtual environment:  
         `virtualenv -p python2 env`  
         `source env/bin/activate`  
         `(env) $ pip install -r requirements.txt`  
         Leave virtual environment:
         `(env) $ deactivate`  
    9. Test the the feed fetcher:  
        `./env/bin/python ./feedfetcher.py`  
        You should see your feeds scrolling through. Check your configured Mattermost channel for the new feeds.  
        If everything works fine:
    10. a) Start feedfetcher with nuhup:    
        `nohup ./env/bin/python ./feedfetcher.py &`  
        b) Alternatively: Start feedfetcher with Supervisor:  
          - `sudo cp Rss-Atom-Feed-Integration-for-Mattermost.conf.sample /etc/supervisor/conf.d/mRss-Atom-Feed-Integration-for-Mattermost.conf`  
          - Edit the supervisor configuration file: `sudo nano /etc/supervisor/conf.d/Rss-Atom-Feed-Integration-for-Mattermost.conf`
          and change paths in `command=` and `directory=` to suit your environment.  
          - Tell Supervisor to look for any new or changed program configurations:  
          `sudo supervisorctl reread`
          - Followed by telling it to enact any changes with:  
          `sudo supervisorctl update`  
        Refer to [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps)
        for more information about Supervisor.  

## Microsoft Windows Install
This integration also works with Microsoft Windows:  
- Download Python 2.7 from [Python.org](https://www.python.org/downloads/) and install it  
- Download mattermost_integration_rss from [Github](https://github.com/bitbackofen/mattermost_integration_rss/archive/master.zip) or get it using `git clone https://github.com/bitbackofen/mattermost_integration_rss.git`  
- Extract the archive to a directory of your choice if you downloaded archive.zip.  
- Start a command prompt and cd into your Python installation directory: e.g. `cd c:\python27`  
- Install requirements using `Scripts\pip.exe install -r \path\to\mattermost_integration_rss\requirements.txt`  
- `cd \path\to\mattermost_integration_rss\`  
- Start the Script:  
  `C:\Python27\python.exe feedfetcher.py` (change `C:\Python27\` if you installed Python elsewhere).  

## Linux/Ubuntu 14.04 Update
1. cd into your mattermost_integration_rss directory:  
    `cd /path/to/Rss-Atom-Feed-Integration-for-Mattermost`
2. Stop feedfetcher:  
    `sudo supervisorctl`  
    `supervisor> stop Rss-Atom-Feed-Integration-for-Mattermost`  
    Exit supervisor (CRTL-c)
2. Update mattermost_integration_rss  
    `git pull origin master`
3. Have a look at `settings.py.sample` for changes.
4. Start the feedfetcher:  
    `sudo supervisorctl`  
    `supervisor> start Rss-Atom-Feed-Integration-for-Mattermost`
