# site-semter

sudo mysql -u root -p 
create database semter; 
create user 'flow'@'localhost' identified by 'flow'; 
grant all privileges on semter.* to 'flow'@'localhost';