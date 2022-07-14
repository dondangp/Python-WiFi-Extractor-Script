#! py
#Created for the use of educational purposes only.
#Wanted to create a python script that automates this process at once.

import subprocess

#    Import the re module so we can make use of regular expressions. 
import re


command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()


profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

#contains wifi username/pw
wifi_list = []

#details of wi-fi password
if len(profile_names) != 0:
    for name in profile_names:
      #Wifi will be set to wifi_list
        wifi_profile = {}
      
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        #Absent scenarios, ignore if not absent.
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            #   assigning ssid to wifi profile
            wifi_profile["ssid"] = name
            #    "key=clear" command for password if not absent
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            #    Again run the regular expression to capture the 
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            
            #    Checking for Wifi Password, but if they dont will be none.
            if password == None:
                wifi_profile["password"] = None
            else:
               
                wifi_profile["password"] = password[1]
           
            wifi_list.append(wifi_profile) 

for x in range(len(wifi_list)):
    print(wifi_list[x]) 
