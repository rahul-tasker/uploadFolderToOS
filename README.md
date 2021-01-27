# uploadFolderToOS
zip a file directory and upload to Oracle Cloud Object Storage Bucket using Oracle Cloud Infrastructure REST API and Python SDK

# Prerequisites
- oci-cli (https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- Pre-created oci-cli config file (~/.oci/config). 
- You can create by `oci setup config` command and assumed DEFAULT profile in the `~/.oci` path. To use a different path and profile, the `start.py` and `stop.py` files must be edited to reflect those changes.
- Python 3 and above (https://realpython.com/installing-python/)
- oci python SDK (https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/installation.html)

# How to use
1. Clone this repository.

2. Open objectStorageUpload.py file and edit # Specify your config file section and directory path accordingly.

3. Errors will be emitted to the standard output.  Redirect it to the file if you need record logs.

4. There is no scheduler included in the script. Please use cron or othe scheduler as you need. 
    - Exapmple of crontab entry to revoke every 0 am 
    ```
    0 * * * cd /home/opc; python3 -u /home/opc/objectStorageUpload/objectStorageUpload.py > /home/opc/log/run_date +%Y%m%d-%H%M%S.log 2>&1
    ```
