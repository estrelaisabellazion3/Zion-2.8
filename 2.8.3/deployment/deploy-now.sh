#!/bin/bash
export SSHPASS='12345abcd'
exec ./deploy-ssh-production.sh "$@"
