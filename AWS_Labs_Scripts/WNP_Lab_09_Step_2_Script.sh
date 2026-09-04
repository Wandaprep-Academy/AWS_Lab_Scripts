#!/bin/bash
# Update and install Apache
sudo dnf update -y
sudo dnf install -y httpd
sudo systemctl enable httpd
sudo systemctl start httpd
# Create a test page
sudo echo "<html> <head><title>Wandaprep Academy</title></head> <body style='font-family: Arial; text-align:center; margin-top:100px;'> <h1>Welcome to Wandaprep Academy EC2 Demo</h1> <p>Your Apache web server is running successfully.</p> </body> </html>" > /var/www/html/index.html
