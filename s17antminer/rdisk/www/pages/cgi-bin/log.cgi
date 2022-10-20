#!/bin/sh -e

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
EOH

echo 'log_type=['\"`find /nvdata -maxdepth 2 -type d | grep "/nvdata/[0-9][0-9][0-9][0-9]-[0-9][0-9]/[0-9^][0-9]"`\"] | sed 's/ /","/g'
#echo 'log_type = ['`find /nvdata -maxdepth 2 -type d | grep "/nvdata/[0-9][0-9][0-9][0-9]-[0-9][0-9]/[0-9][0-9]"`]

cat <<EOT
function f_submit_log_download() {
    data_str = '';
    var earliest = '';
    var latest = '';
    var choosen_cnt = 0;
    for(j = 0; j < log_type.length; j++) {
      if(document.getElementById("ant_log_date_"+j).checked) {
        data_str += log_type[j] + ' ';
        if (earliest == '')
        {
            earliest = log_type[j];
        }
        if (latest == '')
        {
            latest = log_type[j];
        }

        if (log_type[j] > latest)
        {
            latest = log_type[j];
        }
        if (log_type[j] < earliest)
        {
            earliest = log_type[j];
        }
        choosen_cnt++;
      }
    }
    var earliest_items = earliest.split('/');
    var latest_items = latest.split('/');
    var tar_name = 'antminer_log_backup_';
    if (choosen_cnt == 1)
    {
        tar_name = tar_name + earliest_items[2] + '-' + earliest_items[3];
    }
    else if (choosen_cnt > 1)
    {
        tar_name = tar_name + earliest_items[2] + '-' + earliest_items[3] + '_' + latest_items[2] + '-' + latest_items[3];
    }
    else
    {
        alert("please choose one log item!");
        return;
    }

    // add tar file name and send to create_log_backup.cgi.
    data_str += tar_name;
    tar_name += '.tar';
    var maincont = document.getElementById("maincontent");
    var tar_location = '<form action="/log/' + tar_name + '">';
    var main_html = '<fieldset class="cbi-section">' + '<p>Save backup to PC.</p>' + '<table>' + '<tr>' + '<td>' + tar_location;
    main_html += '<input class="cbi-button cbi-button-down" type="submit" name="save" value="Save" />' + '</form>' + '</td>' + '</tr>' + '</table>' + '</fieldset>';
 
    jQuery.ajax({
        url: '/cgi-bin/create_log_backup.cgi',
        type: 'POST',
        timeout: 30000,
        data: data_str,
        dataType: 'json',
        cache: false,
        success: function(data) {
            maincont.innerHTML = main_html;
        },
        error: function(data) {
            maincont.innerHTML = main_html;
        }
    });
}

function f_select_all_log(thisobj) {
        var i = 0;
        var id = "";

        if(thisobj.c==1) {
            thisobj.c=0;
            thisobj.checked=0
        }else{
            thisobj.c=1;
        }

        for(i = 0; i < log_type.length; i++) {
            id = "ant_log_date_" + i;
            obj = document.getElementById(id);
            obj.checked = thisobj.checked;
            obj.c = thisobj.c;
        }
}

</script>
<title>Ant Miner</title>
</head>
<body class="lang_en">
   <p class="skiplink">
      <span id="skiplink1"><a href="#navigation">Skip to navigation</a></span>
      <span id="skiplink2"><a href="#content">Skip to content</a></span>
   </p>
   <div id="menubar">
      <h2 class="navigation"><a id="navigation" name="navigation">Navigation</a></h2>
      <div class="clear"></div>
   </div>
   <div id="menubar" style="background-color: #0a2b40;">
      <div class="hostinfo" style="float: left; with: 500px;">
         <img src="/images/antminer_logo.png" width="92" height="50" alt="" title="" border="0" />
      </div>
      <div class="clear"></div>
   </div>
   <div id="maincontainer">
      <div id="tabmenu">
         <div class="tabmenu1">
            <ul class="tabmenu l1">
               <li class="tabmenu-item-status"><a href="/index.html">System</a></li>
               <li class="tabmenu-item-system"><a href="/cgi-bin/minerConfiguration.cgi">Miner Configuration</a></li>
               <li class="tabmenu-item-system active"><a href="/cgi-bin/log.cgi">Log Configuration</a></li>
               <li class="tabmenu-item-network"><a href="/cgi-bin/minerStatus.cgi">Miner Status</a></li>
               <li class="tabmenu-item-system"><a href="/network.html">Network</a></li>
            </ul>
            <br style="clear: both" />
			<!--
            <div class="tabmenu2">
               <ul class="tabmenu l2">
                  <li class="tabmenu-item-system active"><a href="/cgi-bin/log.cgi">General Settings</a></li>
                  <li class="tabmenu-item-system"><a href="/cgi-bin/minerAdvanced.cgi">Advanced Settings</a></li>
               </ul>
               <br style="clear: both" />
            </div>
			-->
         </div>
      </div>
      <div id="maincontent">
         <noscript>
            <div class="errorbox">
               <strong>Java Script required!</strong><br /> You must enable Java Script in your browser or LuCI will not work properly.
            </div>
         </noscript>
         <h2 style="padding-bottom:10px;"><a id="content" name="content">Miner Log Configuration</a></h2>
         <div class="cbi-map" id="cbi-cgminer">
            <fieldset class="cbi-section" id="cbi_msg_bmminer_fieldset" style="display:none">
               <span id="cbi_msg_bmminer" style="color:red;"></span>
            </fieldset>
            <fieldset class="cbi-section" id="cbi_apply_bmminer_fieldset" style="display:none">
               <img src="/resources/icons/loading.gif" alt="Loading" style="vertical-align:middle" />
               <span id="cbi-apply-cgminer-status">Waiting for changes to be applied...</span>
            </fieldset>
            <fieldset class="cbi-section" id="cbi-cgminer-cgminer">
               <div class="cbi-section-descr"></div>
               <fieldset class="cbi-section" id="cbi-cgminer-default" style="display">
                  <legend>Download</legend>
				  <div class="cbi-value">
					 <label class="cbi-value-title" for="keep">log date</label>
           <input type="radio" id="select_all_id" name="select_all" value="0" onclick="f_select_all_log(this);" c="0" />choose all
					 <div class="cbi-value-field" id="miner_log_date">
					 </div>
				  </div>				  
               </fieldset>
               <br />
            </fieldset>
            <br />
         </div>
         <div class="cbi-page-actions">
            <input class="cbi-button cbi-button-save right" type="button" onclick="f_submit_log_download();" value="Download" />
         </div>
         <div class="clear"></div>
      </div>
   </div>
   <div class="clear"></div>
   <div style="text-align: center; bottom: 0; left: 0; height: 1.5em; font-size: 80%; margin: 0; padding: 5px 0px 2px 8px; background-color: #918ca0; width: 100%;">
      <font style="color:#fff;">Copyright &copy; 2013-2014, Bitmain Technologies</font>
   </div>
</body>
                  <script type="text/javascript">
                      var div = document.getElementById("miner_log_date")
                      div.innerHTML = ''
                      for(j = 0; j < log_type.length; j++) {
                         div.innerHTML += '<input type="radio" id="ant_log_date_' + j +'" name="ant_log_date_' + j + '" value="0" onclick="if(this.c==1){this.c=0;this.checked=0}else{this.c=1}"   c="0"/>'+log_type[j]+'<br>';
                      } 
     
                  </script>
</html>
EOT
