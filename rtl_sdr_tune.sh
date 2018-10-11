#!/bin/#!/usr/bin/env bash

rtl_fm -f ${1}M -M ${2} -s 200K -l 1 -r 48K | aplay -t raw -r 48000 -f S16_LE
