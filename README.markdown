VTRNK Radio Server
A server-side implementation of an internet radio streaming service built with Liquidsoap for audio streaming and playlist management. This repository contains configuration templates and web interface styles, showcasing skills in server-side scripting, configuration management, and deployment on Ubuntu.
Project Structure

liquidsoap/: Liquidsoap configuration templates (no sensitive data).
radio-template.liq: Sample configuration file (replace with your own parameters).


web/css/: Styles for the web interface.
styles.css: CSS for buttons and UI components.



Requirements

Liquidsoap (installed at ~/.opam/4.14.0/bin/liquidsoap).
Python virtual environment (venv/ for dependencies).
Ubuntu 24.04+ (or compatible OS).

Setup Instructions

Activate the virtual environment:source /home/beasty197/projects/vtrnk_radio/venv/bin/activate


Run Liquidsoap with your local configuration (not included in this repo):/home/beasty197/.opam/4.14.0/bin/liquidsoap liquidsoap/radio.liq


Configure .env or local config files with your credentials (excluded from git).

Notes

All sensitive data (passwords, tokens) is stored locally and excluded via .gitignore for security.
Use radio-template.liq as a base and add your own parameters.
This project demonstrates proficiency in Linux server management, Liquidsoap scripting, and secure configuration practices.

License
MIT
