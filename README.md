# GitLab Integration Service for RSS-feeds

This integrations service posts RSS feeds into specific Mattermost channels by formatting output from html to to text 
via [Mattermost's incoming webhooks](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md).

## Requirements

To run this integration you need:

1. A **network connected device running python** like Raspberry Pi or any other Linux device wich support python and the required packages  
2. A **[Mattermost account](http://www.mattermost.org/)** where [incoming webhooks are enabled](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md#enabling-incoming-webhooks)

### Linux/Ubuntu 14.04 Install

The following procedure shows how to install this project on a Linux device running Ubuntu 14.04. 
The following instructions work behind a firewall so long as the device has access to your Mattermost instance. 

To install this project using a Linux-based device, you will need Python 2.7 or a compatible version. 
Other compatible operating systems and Python versions should also work. 

Here's how to start:

1. **Set up your Mattermost instance to receive incoming webhooks**
 1. Log in to your Mattermost account. Click the three dot menu at the top of the left-hand side and go to 
 **Account Settings** > **Integrations** > **Incoming Webhooks**.
 2. Under **Add a new incoming webhook** select the channel in which you want GitLab notifications to appear, then 
 click **Add** to create a new entry.
 3. Copy the contents next to **URL** of the new webhook you just created 
 (we'll refer to this as `https://<your-mattermost-webhook-URL>`).

2. **Set up this project to run on your Linux device**
 1. Set up a **Linux Ubuntu 14.04** server either on your own machine or on a hosted service, like AWS.
 2. **SSH** into the machine, or just open your terminal if you're installing locally.
 3. Confirm **Python 2.7** or a compatible version is installed by running:
    - `python --version` If it's not installed you can find it [here](https://www.python.org/downloads/)
 4. Install **pip** and other essentials:
    - `sudo apt-get install python-pip python-dev build-essential`
 5. Clone this GitHub repo:
    - `git clone https://gitlab.com/m-busche/mattermost_integration_rss.git`
    - `cd mattermost-integration-rss`
 6. Install integration requirements:
    - `sudo pip install -r requirements.txt`
 7. Copy sample file `settings.py.sample`:
    - `cp settings.py.sample settings.py`
 8. Edit `settings.py` to suit your requirements:
    - `nano settings.py`
    - Save your changes (F2) and exit nano (CRTL-X)
 7. Test the server:
    - `python ./feedfetcher.py start`
    - You should see your feeds scrolling through. Check your configured Mattermost channel for the new feeds. 
    - If everything works fine:
 8. Start feedfetcher as daemon:
    - `crontab -e`
    - Scroll down an add 1 line:
    - `@reboot  python /path-to-mattermost_integration_rss/feedfetcher.py start`
    
    
    

