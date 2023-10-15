# HexMail
HexMail is a discord bot that connects your Gmail account to your discord server. It allows you to receive and send emails from discord channels using Gmail API and give notification using publisher-subscriber model.

## Table of Contents
1. Features
2. Technologies Used
3. Setting up Discord Bot Host
4. Setting up Gmail API for Discord Bot Host
5. Setting up Pub/Sub for Discord Bot Host
6. How to Setup Project
7. License

## Features
1. HexMail is a bot which joins your discord servers, and creates channels in your discord server and manages your emails in them.
2. HexMail uses the publisher-subscriber model along with the Gmail API, so you will be notified whenever you receive a new email.
3. HexMail can maintain multiple emails in a single server.
4. Manages different channels like inbox, sent, drafts etc. of every linked email.
5. HexMail supports discord server rules to manage read/write permissions for specific users.

## Technologies Used
HexMail is built with the following technologies:
1. Python
2. discord API
3. Gmail API
4. Publisher Subscriber Model
5. Google Cloud Platform
6. PostgreSQL

### Setting up discord bot.
To set up HexMail as a discord bot host, you need to have a Discord account on the `Discord Developer Portal`.

You can follow these steps to set up a discord bot:
1. Go to the `Discord Developer Portal` and create an application.
2. Go to the `Bot` tab and click on `Add Bot`.
3. Give your bot a name and an icon, and copy the token.
4. Go to the `OAuth2` tab and select `bot` as the scope and `Administrator` as the permission.
5. Copy the generated URL and paste it in your browser to invite the bot to your server.

- For more help search on internet on how to set up Discord bot.
    > Only bot host need to follow this Section.

### Setting up GMAIL API for discord bot host.
To set up HexMail with the Gmail API, you need to have a Google account and enable the Gmail API service.

You can follow these steps to set up the Gmail API:
1. Go to the `Google Cloud Platform` Console and create a project.
2. Go to the `APIs & Services` dashboard and click on `Enable APIs and Services`.
3. Search for `Gmail API` and click on `Enable`.
4. Go to the `Credentials` tab and click on `Create Credentials`.
5. Select `OAuth client ID` as the credential type and choose `Desktop App` as the application type.
6. Give your application a name and add your redirect URI.
7. Click on `Create` and download the JSON file with your credentials.
8. Copy you token in `<project_directory>/gmail/credentials.json`.[*create if not present*]

- Visit this website to know more about getting gamil token [Gmail Help](https://developers.google.com/gmail/api/auth/web-server)

    > Only bot host need to follow this Section.

### Setting up Pub/Sub for discord bot host.
To set up HexMail with Pub/Sub, you need to have a Google account and enable the Pub/Sub service.

You can follow these steps to set up Pub/Sub:

1. Go to the `Google Cloud Platform` Console and select your project.
2. Go to the `APIs & Services` dashboard and click on `Enable APIs and Services`.
3. Search for `Cloud Pub/Sub API` and click on `Enable`.
4. Go to the `Pub/Sub` dashboard and click on `Create Topic`.
5. Give your topic a name and click on `Create`.
6. Click on your topic and go to the `Permissions` tab.
7. Click on `Add Member` and add the service account `gmail-api-push@system.gserviceaccount.com` with the role `Pub/Sub Publisher`.
8. Go to the `Gmail API` dashboard and click on `Manage User Access`.
9. Click on `Configure consent screen` and select `External` as the user type.
10. Fill in the required information and click on `Save and Continue`.
11. Click on `Add or Remove Scopes` and add the scope `https://mail.google.com/`.
12. Click on `Save and Continue` and then on `Back to Dashboard`.
13. Click on `Test Users` and add your email address as a test user.
14. Go to the URL [Pub/Sub](https://developers.google.com/oauthplayground/) and sign in with your email address.
15. On the left panel, select the Gmail API v1 and the scope `https://mail.google.com/`.
16. Click on `Authorize APIs` and then on `Exchange authorization code for tokens`.
17. Copy you token in `<project_directory>/pub_sub/pub_sub_token.json`. [*create if not present*]

- Visit this website to know more about getting gamil token [Pub/Sub Help](https://developers.google.com/gmail/api/guides/push)
    > Only bot host need to follow this Section.

#### *[!WARNING] This project uses a discord bot, gmail api, and pub/sub for notification. These features require access to actual accounts and data, which may pose security risks if not configured properly. Please follow the best practices and guidelines from reliable sources when setting up these features. Do not share your credentials or tokens with anyone, and use secure authentication methods and encryption. For more information, see website mentioned above in their respective sections.*

## How to Setup Project.
1. Get project files to local drive by: 
    - Download this project and then extract it.
    - Fork the repository and clone project with command `git clone <project_link>` on local drive
2. Nevigate to downloaded or Cloned folder and open it in code editor.
3. Initiate a new virtual Environment by command `python -m venv <environment_name>`.
4. Activate virtual environment by command `<environmane_name>\Script\activate` 
    > Command in step 4 is only for windows. Linux and macOS have different commands.

    > Steps 3 and 4 are not compulsory but recommended. And virtual Environment can be of your choice.
5. Install required modules by running command `python -m pip install -r requirements.txt`.
6. Install `PostgreSQL` and set up database.
    > There are 2 tables in database.
        
    > 1st is `users` which saves basic info. of users and discord info.

    - discord_id
    - name
    - discriminatior

    > 2nd table is `user_token` which stores users token and gmail info.

    - fk_user (Foriegn Key => linked to discord_id in 1st table)
    - histor_id
    - watch_exp
    - email
    - token

7. Create `.env` file in main folder and save add some Environment Variabels:
    - DB_NAME : Name of Database
    - DN_UNAME : Name of user of Database
    - DB_PASS : Password of Database
    - DISCORD-BOT-TOKEN : TOKEN provided by discord Developer portal for the Bot

### Setup is complete and you can run the project with command `python run.py`.

### Contributing
HexMail is an open source project and welcomes contributions from anyone who wants to improve it.

To contribute to HexMail, you can follow these steps:
1. Fork this repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your feature or bug fix.
4. Make your changes and commit them with a descriptive message.
5. Push your changes to your forked repository.
6. Create a pull request from your forked repository to this repository.
7. Wait for your pull request to be reviewed and merged.

### [License](https://github.com/thunderbolt181/HexMail/blob/master/LICENSE) 

>*[!DISCLAIMER] The author of this project is not liable for any problems or damages that may occur from the use or misuse of this project. The user is solely responsible for following the security guidelines and best practices when setting up and using this project. The user assumes all risks and consequences of using this project.*