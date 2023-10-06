sudo docker run --restart="unless-stopped" -t --name stream \
  -v /home/pi/shared/stream:/user-data --privileged \
  --group-add video --user `id -u`:`id -g` \
  -e LICENSE_KEY=74kuQFDG9U -e TOKEN=0fc3b79ea02aa0262aa57f90affa1613dca33de4 \
  platerecognizer/alpr-stream:raspberry

sudo docker run --restart="unless-stopped" -t --name stream \
-v /mnt/c/Users/ASUS/stream:/user-data \
-e LICENSE_KEY=74kuQFDG9U -e TOKEN=0fc3b79ea02aa0262aa57f90affa1613dca33de4 \
platerecognizer/alpr-stream