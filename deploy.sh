
echo "source /var/www/html/env/bin/activate

cd /var/www/html/tfg

git pull origin master 

python manage.py makemigrations 
python manage.py migrate 
sudo supervisorctl restart tfg
 
"|ssh -i /home/gerges/Downloads/Tfg.pem ubuntu@52.25.102.58