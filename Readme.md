# Reminder
Reminder is a discord bot that DMs me when I get online after school (past 1400) the work I have due that is on my schoolwork Trello page.

## ENV File
The env file is structured as:
```
TOKEN=<discord bot token>
INVITE_LINK=<invite link for bot>
USER_ID=<ID of user to watch and DM>
GUILD_ID=<ID of guild user is in>
TRELLO_TOKEN=<trello api token>
TRELLO_KEY=<trello api key>
TRELLO_BOARD=<trello board id>
TRELLO_LIST=<trello list name to get cards from>
# \/ The api link with filled in variables \/
TRELLO_BOARD_URL=https://api.trello.com/1/boards/${TRELLO_BOARD}/lists?key=${TRELLO_KEY}&token=${TRELLO_TOKEN}
# \/ The python .format string for the list \/
TRELLO_LIST_URL=https://api.trello.com/1/lists/{}/cards?key=${TRELLO_KEY}&token=${TRELLO_TOKEN}