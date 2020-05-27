#!/bin/python3

import importlib

def main():
	importlib.invalidate_caches()
	other = importlib.import_module("strangename")
	
	other.echo("hi")

main()
