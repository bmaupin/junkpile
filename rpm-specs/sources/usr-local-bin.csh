if ( "${path}" !~ */usr/local/bin* ) then
	set path = ( /usr/local/bin $path )
endif
if ( "${path}" !~ */usr/local/sbin* ) then
	if ( `id -u` == 0 ) then
		set path = ( /usr/local/sbin $path )
	endif
endif
