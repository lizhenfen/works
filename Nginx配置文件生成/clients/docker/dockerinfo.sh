#!/bin/bash

echo -e "{\n"
echo  -e "\t\"data\":[\n"
FIRST=0
for d in `docker ps | awk -F" " 'NR>1{print $NF}'`
do 
    dname=${d}
    did=`docker inspect ${d} | grep -w "Id" | awk -F":" '{print $2}' | tr -d '",'`
    pid=`docker inspect ${d} | grep -w "Pid" | awk -F":" '{print $2}' | tr -d ','`
    natport=`docker inspect ${d} | grep -w "HostPort" | uniq | awk -F":" '{print $2}' | tr -d '"'`
    port=`docker inspect ${d} | grep -w "HTTP_PORT" | awk -F"=" '{print $2}' | tr -d '",'`
    if [[ ${natport} != '' ]];then
        docker_port=${natport}
    else
        docker_port=${port}
    fi
    [[ ${FIRST} == 1 ]]  && echo -e "\t,\n"
    FIRST=1
    echo -e "\t\t{\n"
    echo -e "\t\t\"dname\":\"${dname}\",\n"
    echo -e "\t\t\"did\":\"${did}\",\n"
    echo -e "\t\t\"pid\":\"${pid}\",\n"
    echo -e "\t\t\"pid\":\"${pid}\",\n"
    echo -e "\t\t\"port\":\"${docker_port}\"\n"
    echo -e "\t\t}\n"
   

done
echo -e "\t]\n"
echo -e "}"