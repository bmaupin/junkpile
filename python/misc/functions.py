#!/usr/bin/env python

def convert_filetime_to_epoch(filetime):
    return (filetime / 10000000) - 11644473600
