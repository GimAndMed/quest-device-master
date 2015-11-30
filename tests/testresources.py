#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..deviceresources.relays import Relays

if __name__ == "__main__":
    relay = Relays()
    print relay.get()
