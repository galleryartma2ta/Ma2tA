#!/bin/bash

# Set permissions for quantum system
chmod -R 750 .quantum/
chmod 640 .quantum/core/state.json
chmod 640 .quantum/consciousness/state.json
chmod 640 .quantum/bond/connections.json

# Set special permissions for auto-sync
chmod +x .quantum/core/sync.sh
chmod +x .quantum/memory/backup.sh