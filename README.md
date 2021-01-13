# Nix Channel Watcher

## What is this?

This is a really simple Python script that checks the status of one or more
Nix channels. If the channel has been updated (i.e. the Git revision has
changed) then the files in `<channel-name>.hooks/` are run.

This is meant to be run periodically, e.g. with a systemd timer or a cron job.

## How do I use it?

Channels go in `channels.txt`. Hooks for when a channel has been updated go
in `<channel-name>.hooks/` (you can use symlinks if you want). It's pretty
straightforward.
