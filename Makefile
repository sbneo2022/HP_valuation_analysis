# Makefile for running Streamlit app

.PHONY: help run

help:
	@echo "Usage:"
	@echo "  make run       Run the Streamlit application"
	@echo "  make help      Show this help message"

run:
	streamlit run app.py
