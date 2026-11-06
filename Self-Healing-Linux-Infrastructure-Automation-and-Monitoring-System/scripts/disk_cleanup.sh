#!/bin/bash

apt clean
journalctl --vacuum-time=7d
