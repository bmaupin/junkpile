if ! echo ${PATH} | /bin/grep -q /usr/local/bin ; then
	PATH=/usr/local/bin:${PATH}
fi
if ! echo ${PATH} | /bin/grep -q /usr/local/sbin ; then
	if [ `/usr/bin/id -u` = 0 ] ; then
		PATH=/usr/local/sbin:${PATH}
	fi
fi
