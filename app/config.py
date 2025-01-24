from dotenv import load_dotenv
from app import app
from flask import render_template
from flask import Flask, request, jsonify, redirect, url_for, flash, send_from_directory, current_app
from markupsafe import Markup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import re
import os
import asyncio
import aiohttp
import setproctitle
setproctitle.setproctitle("MeuProcessoPython")
email = 'sigaav2@gmail.com'
load_dotenv()  # Carrega as variáveis do arquivo .env
senha = os.getenv('APP_PASSWORD')
