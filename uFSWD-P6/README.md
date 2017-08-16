# Server Configuration to deploy web-server on AWS


# Server Information
 - IP Address: 35.166.245.207
 - SSH Port: 2200
 - URL: www.karthiks.info
 - Json endpoint:
   - Catalog: www.karthiks.info/api/v1/catalog
   - Items: www.karthiks.info/api/v1/catalog
 - Command to ssh as grader:
   ```sh
   #Where grader.key data is provided the candidate
   ssh -p 2200 -i grader.key grader@karthiks.info
   ```  

# Steps Performed
 - Created new instance of AWS Lightsail
 - Generated a static ip
 - Registered the IP on Google domains for the website
 - Firewall: Configure network permissions on AWS Console
 - Connected the ssh session using AWS Console
 - Downloaded the authorization key from the console
 - Updated the existing packages:
   ```sh
   sudo apt-get update && sudo apt-get upgrade sudo apt-get dist-upgrade
   ```
 - To add new user:
   ```sh
   # Create a new user
   sudo useradd -m -s /bin/bash grader -d /home/grader
   # Adds the user grader to sudo group
   sudo usermod -aG sudo grader
   # Providing sudo access to grader without password
   sudo echo "grader ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/90-cloud-init-users
   # Sudo'ing as grader
   sudo su - grader
   # Creating new ssh keys
   ssh-keygen
   cd .ssh
   # Authorizing the generated keys
   cp id_rsa.pub authorized_keys
   # printing the key on screen for reference
   cat id_rsa # Copy the data for reference
   # exiting the grader shell
   exit
   ```
 - Installed the required tools:
   - Python tools:
   ```sh
   sudo apt-get install python3 python3-pip virtualenv
   ```
   - NTP Tools:
   ```sh
   sudo apt-get install ntp ntpstat
   ```
   - PostgreSQL:
   ```sh
   sudo apt-get install postgresql libpq-dev
   ```
   - Apache tools:
   ```sh
   sudo apt-get install apache2 libapache2-mod-wsgi
   ```
 - Update the SSH port from 22 to 2200:
   - Edit /etc/ssh/sshd_config to change from Port 22 to 2200
     ```sh
     # Change port to 2200
     sudo sed "/^Port/ s/[^ ]*[^ ]/2200/2" -i /etc/ssh/sshd_config
     # Disable root login
     sudo sed "/^PermitRootLogin/ s/[^ ]*[^ ]/no/2" -i /etc/ssh/sshd_config
     ```
   - Restart ssh service
     ```sh
     sudo service ssh restart
     ```
 - Set timezone to UTC:
   ```sh
   sudo timedatectl set-timezone UTC
   ```
 - Perform System reboot and reconnect:
   ```sh
   sudo reboot
   # wait for system to reboot
   ssh -i <sshkey>.pem -p 2200 ubuntu@35.166.245.207
   ```
 - Project Setup:
   - Clone the git repository:
     ```sh
     git clonehttps://github.com/karthiksrinivasan/uFSWD-P4.git
     ```
   - Setup production database:
     ```sh
     sudo -u postgres createuser -P item_catalog
     # Enter password  - udacity
     sudo -u postgres createdb -O item_catalog catalog
     ```
   - Setup virtual environment:
     ```sh
     virtualenv -p python3 env
     ```
   - Install python library requirements:
     ```sh
     env/bin/pip install -r requirements
     ```
   - Setup the server to be of Production configuration:
     ```sh
     export ITEM_CATALOG_SERVER='app.config.ProductionConfig'
     ```   
   - Initialize the database
     ```sh
     ./run.py db_initialize
     ```
  - Configure Apache to forward requests to 8080 for port 80
    - Create a new config file with the following content
      ```sh
      sudo vim /etc/apache2/sites-available/item_catalog.conf
      ```
      ```
      LoadModule proxy_module modules/mod_proxy.so
      LoadModule proxy_http_module modules/mod_proxy_http.so
      <VirtualHost *:80>
          ServerName www.karthiks.info

          ServerAdmin udacity@karthiks.info

          # Define WSGI parameters. The daemon process runs as the www-data user.
          WSGIDaemonProcess item_catalog user=www-data group=www-data threads=5
          WSGIProcessGroup item_catalog
          WSGIApplicationGroup %{GLOBAL}
          ProxyPreserveHost On
          ProxyRequests Off
          ProxyPass / http://localhost:8080/
          ProxyPassReverse / http://localhost:8080/
          ErrorLog ${APACHE_LOG_DIR}/error.log
          LogLevel warn
          CustomLog ${APACHE_LOG_DIR}/access.log combined
      </VirtualHost>
      ```
    - Disable existing default config and enable new config
      ```sh
      sudo  a2dissite 000-default.conf
      sudo  a2ensite item_catalog.conf
      ```
    - Enable Proxy module
      ```sh
      sudo a2enmod proxy_http
      ```
    - Restart Apache service
      ```sh
      sudo service apache2 restart
  - Run the server
    ```sh
    ./run.py runserver -h 0.0.0.0 -p 8080      
    ```
