# PropHunt Discord Taunt Adder

This repository contains the source code for the Discord Prophunt Sound Management bot. The bot listens for the !add command. When a user executes !add, it processes all attachments in the message. If an attachment is a video, it converts it to an audio file and uploads it to PufferPanel for use in Prophunt.

The application is designed to be deployed using Docker.

## Getting Started
Follow the instructions below to set up and run the application.

### Setup
Docker: Make sure you have Docker installed on your system. For installation instructions, visit Docker documentation.

#### Environment Variables:

 - PUFFERPANEL_URL: The URL of the PufferPanel instance.
 - DISCORD_TOKEN: Discord bot token.
 - PUFFERPANEL_USER: PufferPanel username for authentication.
 - PUFFERPANEL_PASS: PufferPanel password for authentication.
 - SERVER_ID: ID of the server in PufferPanel.
 - SOUND_DIRECTORY: Directory in which to store sound files.
 - Docker Compose
 - Clone this repository to your local machine.

### Docker CLI
```shell
docker run -d --restart=unless-stopped \
-p <HOST_PORT>:<CONTAINER_PORT> \
-e PUFFERPANEL_URL=<PUFFERPANEL_URL> \
-e DISCORD_TOKEN=<DISCORD_TOKEN> \
-e PUFFERPANEL_USER=<PUFFERPANEL_USER> \
-e PUFFERPANEL_PASS=<PUFFERPANEL_PASS> \
-e SERVER_ID=<SERVER_ID> \
-e SOUND_DIRECTORY=<SOUND_DIRECTORY> \
your-image-name:tag
```
### Usage
!add: Initiates the process of adding sound files to PufferPanel for use in Prophunt. All attachments in the message will be added.
