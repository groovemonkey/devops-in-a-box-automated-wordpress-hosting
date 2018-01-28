# 1. Digital Ocean API Setup

1. Log into your DigitalOcean dashboard.
2. Click the "API" item in the top menu.
3. Under "Personal access tokens", click "Generate New Token."
4. Create a read/write token and name it something you'll remember.
5. Copy the token and create a file at keys/digitalocean.token The file should look like this (substitute your token for the random text after the equals sign):

    export DO_TOKEN=08ff334afaffddd000000000fffffffffaaaaaaaaaaaaaaaaaa8888800fffaaa

The automation scripts in this course will look for the DO_TOKEN environment variable, so make sure you have it set before running automation scripts. You can set the variable from this file by running:

    source keys/digitalocean.token

You'll have to do this in each shell session that you want to run automation scripts from. You can verify that the environment variable has been set in your shell session (a single shell window) by running

    echo $DO_TOKEN

Now you can run DigitalOcean automation scripts to your heart's content!

