---
title: CUPS
---

## Useful commands

#### Print from the command line
```
lp -d printer_name
``` ```
filename
```

Or:
```
command | lp -d printer_name
```


#### Get status of active print jobs (print queue)
```
lpstat
```


#### List available/default printers
```
lpstat -p -d
```


#### Cancel print job
```
cancel job_name
```

Ex:
```
cancel hp_8150-97
```

Or:
```
lprm job_id_number
```

Ex:
```
lprm 97
```


#### Print a test page
- RHEL 5:
    ```
    lp -d *printer_name* /usr/share/cups/data/testprint.ps
    ```

- RHEL 6/Ubuntu 14.04:
    ```
    lp -d *printer_name* /usr/share/cups/data/testprint
    ```


#### Add a printer
```
sudo /usr/sbin/lpadmin -p printer_name -D printer_description -L printer_location -E -v device_uri -P path_to_ppd

```


#### Remove a printer
```
sudo /usr/sbin/lpadmin -x printer_name
```


#### Set a printer as default
```
sudo /usr/sbin/lpadmin -d printer_name
```
