docker run --restart="unless-stopped" -t --name stream \
  -v /home/pi/shared/stream:/user-data --privileged \
  --group-add video --user `id -u`:`id -g` \
  -e LICENSE_KEY=amRcLYCkE7 -e TOKEN=eb1d8153a1e69b23cf1a956c212cba0b18d11dd0 \
  platerecognizer/alpr-stream:raspberry

  docker run --restart="unless-stopped" -t --name stream \
  -v /mnt/c/Users/ASUS/stream:/user-data \
  -e LICENSE_KEY=amRcLYCkE7 -e TOKEN=eb1d8153a1e69b23cf1a956c212cba0b18d11dd0 \
  platerecognizer/alpr-stream
