#!/bin/sh -e

# POST upload format:
# -----------------------------29995809218093749221856446032^M
# Content-Disposition: form-data; name="file1"; filename="..."^M
# Content-Type: application/octet-stream^M
# ^M    <--------- headers end with empty line
# file contents
# file contents
# file contents
# ^M    <--------- extra empty line
# -----------------------------29995809218093749221856446032--^M

file=/dev/$$

trap atexit 0

atexit() {
	rm -rf $file
	umount $file.boot 2>/dev/null || true
	rmdir $file.boot 2>/dev/null || true
	sync
	if [ ! $ok ]; then
	    echo "<h1>System upgrade failed</h1>"
	fi
}

CR=`printf '\r'`

exec 2>/tmp/upgrade_result

IFS="$CR"
read -r delim_line
IFS=""

while read -r line; do
    test x"$line" = x"" && break
    test x"$line" = x"$CR" && break
done

mkdir $file
cd $file

error_handling()
{
    rm $$.tgz
    exit 1
}

#### validity check
cat > $$.tgz
if [ -f $$.tgz ]
then
    tar ztvf $$.tgz | grep "^l" >& /dev/null
    if [ $? -eq 0 ]
    then
        echo "tarball contains symbol link" >> /tmp/upgrade_new.log
        error_handling
    fi
    echo "no symbol link found" >> /tmp/upgrade_new.log
else
    echo "unkown error occurs, can't find tarball" >> /tmp/upgrade_new.log
    error_handling
fi

tar zxf $$.tgz
rm $$.tgz

if [ ! -f runme.sh.sig ]; then
    echo "Cannot Find Signature!!!">> /tmp/upgrade_result
else    
    openssl dgst -sha256 -verify /etc/bitmain-pub.pem -signature  runme.sh.sig  runme.sh >/dev/null  2>&1
    res=$?
		if [ $res -eq 1 ]; then
		    echo "Installer Not Signtured!!!" >> /tmp/upgrade_result
		else
		    if [ -f runme.sh ]; then
			    md5res=`md5sum runme.sh | cut -d ' ' -f 1`
	        grep -w $md5res /etc/blacklist > /dev/null 2>&1
        	mdr=$?
		        if [ $mdr -ne 0 ]; then
		        	sh runme.sh
		        else
		           echo "CANNOT USE THIS RUNME!!!" >> /tmp/upgrade_result
		        fi
				else
		    	if [ -e /dev/mmcblk0p3 ]; then
						mkdir $file.boot
		    		mount /dev/mmcblk0p1 $file.boot
		    		cp -rf * $file.boot/
		    		umount $file.boot
		    		sync
					fi
					if [ -e /dev/mtd8 ]; then
						if [ -e initramfs.bin.SD ]; then
							echo "flash romfs"
							flash_eraseall /dev/mtd8 >/dev/null 2>&1
							nandwrite -p /dev/mtd8 initramfs.bin.SD >/dev/null 2>&1
						fi

						if [ -e uImage.bin ]; then
							echo "flash kernel"
							flash_eraseall /dev/mtd7 2>/dev/null
							nandwrite -p /dev/mtd7 uImage.bin 2>/dev/null
						fi
					fi
			fi
		fi
fi

ant_result=`cat /tmp/upgrade_result`

# CGI output must start with at least empty line (or headers)
printf "Content-type: text/html\r\n\r\n"

cat <<-EOH
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta http-equiv="cache-control" content="no-cache" />
<link rel="stylesheet" type="text/css" media="screen" href="/css/cascade.css" />
<!--[if IE 6]><link rel="stylesheet" type="text/css" media="screen" href="/css/ie6.css" /><![endif]-->
<!--[if IE 7]><link rel="stylesheet" type="text/css" media="screen" href="/css/ie7.css" /><![endif]-->
<!--[if IE 8]><link rel="stylesheet" type="text/css" media="screen" href="/css/ie8.css" /><![endif]-->
<script type="text/javascript" src="/js/xhr.js"></script>
<script type="text/javascript" src="/js/jquery-1.10.2.js"></script>
<script type="text/javascript" src="/js/json2.min.js"></script>
<script>
function f_submit_reboot() {
	jQuery.ajax({
		url: '/cgi-bin/reset_conf.cgi',
		type: 'GET',
		dataType: 'text',
		timeout: 30000,
		cache: false,
		data: {},
		complete: function(data) {
		    setTimeout(function(){
			window.location.href="/index.html";
		    }, 90000);
		}
	});
}
function f_submit_goback() {
	window.location.href="/upgrade.html";
}
</script>
<title>Ant Miner</title>
</head>
EOH

if [ "${ant_result}" == "" ]; then
	echo "<body class=\"lang_en\" onload=\"f_submit_reboot();\">"
else
	echo "<body class=\"lang_en\">"
fi

cat <<-EOB
<p class="skiplink">
<span id="skiplink1"><a href="#navigation">Skip to navigation</a></span>
<span id="skiplink2"><a href="#content">Skip to content</a></span>
</p>
<div id="menubar">
<h2 class="navigation"><a id="navigation" name="navigation">Navigation</a></h2>
<div class="clear"></div>
</div>
<div id="menubar" style="background-color: #0a2b40;">
<div class="hostinfo" style="float:left;with:500px;">
	<img src="/images/antminer_logo.png" width="92" height="50" alt="" title="" border="0" />
</div>
<div class="clear"></div>
</div>
<div id="maincontainer">
	<div id="tabmenu">
	<div class="tabmenu1">
	<ul class="tabmenu l1">
		<li class="tabmenu-item-status active"><a href="/index.html">System</a></li>
		<li class="tabmenu-item-system"><a href="/cgi-bin/minerConfiguration.cgi">Miner Configuration</a></li>
		<li class="tabmenu-item-network"><a href="/cgi-bin/minerStatus.cgi">Miner Status</a></li>
		<li class="tabmenu-item-system"><a href="/network.html">Network</a></li>
	</ul>
	<br style="clear:both" />
	<div class="tabmenu2">
	<ul class="tabmenu l2">
		<li class="tabmenu-item-system"><a href="/index.html">Overview</a></li>
		<li class="tabmenu-item-system"><a href="/administration.html">Administration</a></li>
		<li class="tabmenu-item-admin"><a href="/monitor.html">Monitor</a></li>
		<li class="tabmenu-item-packages"><a href="/kernelLog.html">Kernel Log</a></li>
		<li class="tabmenu-item-startup active"><a href="/upgrade.html">Upgrade</a></li>
		<li class="tabmenu-item-crontab"><a href="/reboot.html">Reboot</a></li>
	</ul>
	<br style="clear:both" />
	</div>
	</div>
	</div>
		<div id="maincontent">
			<noscript>
				<div class="errorbox">
					<strong>Java Script required!</strong><br /> You must enable Java Script in your browser or LuCI will not work properly.
				</div>
			</noscript>
EOB

if [ "${ant_result}" == "" ]; then
	echo "<h2><a id=\"content\" name=\"content\">System Upgrade Successed</a></h2>"
	echo "<fieldset class=\"cbi-section\" id=\"cbi_apply_cgminer_fieldset\" style=\"display:block\">"
	echo "<img src=\"/resources/icons/loading.gif\" alt=\"Loading\" style=\"vertical-align:middle\" />"
	echo "<span id=\"cbi-apply-cgminer-status\">Rebooting System ...<br />&nbsp;<br />(please wait for a few minutes)</span>"
	echo "</fieldset>"
else
	echo "<h2><a id=\"content\" name=\"content\">System Upgrade Failed</a></h2>"
	echo "<fieldset class=\"cbi-section\">"
	echo "<p>"
	cat /tmp/upgrade_result
	echo "</p>"
	echo "<table>"
	echo "<tr>"
	echo "<td>"
	echo "<input class=\"cbi-button cbi-button-link\" type=\"button\" onclick=\"f_submit_goback();\" value=\"Go Back\" />"
	echo "</td>"
	echo "</tr>"
	echo "</table>"
	echo "</fieldset>"
fi

cat <<EOT
			<div class="clear"></div>
		</div>
	</div>
	<div class="clear"></div>
	<div style="text-align: center; bottom: 0; left: 0; height: 1.5em; font-size: 80%; margin: 0; padding: 5px 0px 2px 8px; background-color: #918ca0; width: 100%;">
		<font style="color:#fff;">Copyright &copy; 2013-2018, Bitmain Technologies</font>
	</div>
</body>
</html>
EOT

ok=1
