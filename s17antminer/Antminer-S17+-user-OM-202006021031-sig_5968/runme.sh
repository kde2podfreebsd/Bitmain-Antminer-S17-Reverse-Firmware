#set -x
if [ ! -f cert.pem ]; then
  echo "RUNME: CANNOT FIND CERT!" >> /tmp/upgrade_result
  rm * -rf > /dev/null 2>&1
  exit 1
fi
if [ ! -f cert.pem.sig ]; then
  echo "RUNME: CANNOT FIND CERT SIG!" >> /tmp/upgrade_result
  rm * -rf > /dev/null 2>&1
  exit 2
fi
if [ -e /etc/bitmain-pub.pem ]; then
  openssl dgst -sha256 -verify /etc/bitmain-pub.pem -signature  cert.pem.sig  cert.pem >/dev/null  2>&1 
  res=$?
  if [ $res -ne 0 ]; then
    echo "RUNME: CANNOT VERIFY CERT !" >> /tmp/upgrade_result
    rm * -rf > /dev/null 2>&1
    exit 3
  fi
fi
if [ ! -f fw.tar.gz.sig ]; then
  echo "RUNME: CANNOT FIND FW SIGNATURE!" >> /tmp/upgrade_result
  rm * -rf > /dev/null 2>&1
  exit 4
fi
openssl dgst -sha256 -verify cert.pem -signature  fw.tar.gz.sig  fw.tar.gz >/dev/null  2>&1 
res=$?
if [ $res -ne 0 ]; then
  echo "RUNME: CANNOT VERIFY FW !" >> /tmp/upgrade_result
  rm * -rf > /dev/null 2>&1
  exit 5
fi
mkdir /tmp/mem
mount -t tmpfs tmpfs /tmp/mem
mkdir /tmp/mem/fw 
tar zxvf fw.tar.gz -C /tmp/mem/fw > /dev/null 2>&1
rm fw.tar.gz
cd /tmp/mem/fw
sh runme.sh
sync >/dev/null 2>&1
