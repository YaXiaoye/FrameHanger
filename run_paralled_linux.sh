#!/bin/bash

function cleanTempChromeDriver {
     rm -r /tmp/.com.google.Chrome.*
     rm -r /tmp/.org.chromium.Chromium.*
}

#make sure you have pkill installed
function killChrome {
    pkill chrome
    pkill chromedriver
    pkill Xvfb
}

PASSED=$1
mydir=`dirname $0`


eachRound=25

if   [ -d "${PASSED}" ]
then
    IFS=!
    ARRAY=(`find $1 -type f -printf $1%f! | sort -z`)
    COUNT="0"

    for i in ${ARRAY[*]}; do
        let COUNT++;
    done

    Round=$(( $COUNT/$eachRound + 1))
    echo "Total $COUNT files, Round $Round, each Round $eachRound"
    START=0
    for  (( c=$START; c<$Round; c++ ))
    do
        echo "Round $c Begin"
        for (( k=0; k<eachRound; k++ ))
        do
             cur=$(( $eachRound*$c + $k))
             timeout 120 $mydir/xvfb-run-safe.sh python iframe_injection_detection.py  "${ARRAY[$cur]}" $2 &
        done
        wait
        echo
        echo "Done round $c"
        killChrome
    done

elif [ -f "${PASSED}" ]
then
     $mydir/xvfb-run-safe.sh python iframe_injection_detection.py $1 $2
     killChrome

else echo "${PASSED} is not valid";
     exit 1
fi

cleanTempChromeDriver

echo "Finish ALL, Clean and Exit"


#An example on for the html files in a folder
#/bin/bash ./run_paralled_linux.sh /mnt/sdb1/domcrawl/htmls/10/
