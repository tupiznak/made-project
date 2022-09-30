cd ../backend
docker build -t made22t4/backend:1.0 .
cd ../frontend
docker build -t made22t4/frontend:1.0 .
cd ../logs
docker build -t made22t4/logs:1.0 .

docker volume create made22t4-database
