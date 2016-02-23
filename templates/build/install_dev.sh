#!/bin/sh

rm -f /etc/init.d/@APPNAME@
ln -s /mnt/src/conf/@APPNAME@.service /etc/init.d/@APPNAME@

rm -f /usr/bin/@APPNAME@.sh
ln -s /mnt/src/src/api/@APPNAME@.sh /usr/bin/@APPNAME@.sh

rm -rf /var/www/@APPNAME@
ln -s /mnt/src/src /var/www/@APPNAME@

rm -f /etc/nginx/sites-available/@APPNAME@
ln -s /mnt/src/conf/nginx_default.conf /etc/nginx/sites-available/@APPNAME@
ln -s /etc/nginx/sites-available/@APPNAME@ /etc/nginx/sites-enabled/@APPNAME@

sqlite3 /var/www/@APPNAME@/api/@APPNAME@.db < /var/www/@APPNAME@/api/@APPNAME@.sql
chown -R www-data:www-data /var/www/@APPNAME@/api/@APPNAME@.db

