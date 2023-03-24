# SNOBoard Exporter

SNOBoard-Exporter starts a simple python script that pulls information from storj node api for `node`, `satellite` and `payout` metrics and sends this data to the SNOBoard server where it is aggregated and stored to be available for the mobile app dashboard.

## Usage

* SNOBoard-Exporter can be installed as a docker container or run as a standalone script.
* Make sure you have `-p 14002:14002` in your storagenode container docker run command to allow local connections to your node's api.

### Installation
#### Docker installation
    
##### Run latest build from DockerHub

    docker run -d -e ACCOUNT='cbcc7139de2495dc36604f5a9d2cd4ac' -e NODES_LIST=192.168.188.15:14002,yourdomain.ddns.net:14003 --name snoboard-exporter mb17/snoboard-exporter:latest

       
###### As an environment parameter `NODES_LIST` you need to add a comma seperated list of your node's ip addresses together with their storj api ports. You can add as many nodes into that list as you want. Please download the mobile app for iOS or Android first and create an account in there. Copy your account id and use it inside the docker run command as `-e ACCOUNT='YOUR_PERSONAL_ACCOUNT_ID'`

##### Check the logs
###### After starting the exporter, you should quickly check the logs for errors. If there are none, you should be able to see your nodes in the SNOBoard app after a short time.

    docker logs --follow snoboard-exporter
    
#### Installation without docker
You don't need docker to run the exporter. You can instead just download the app.py file from this repository and run it like this. Note that you also have to set the parameters ACCOUNT and NODES_LIST as environment variables:

    export ACCOUNT=cbcc7139de2495dc36604f5a9d2cd4ac
    export NODES_LIST=192.168.188.15:14002,yourdomain.ddns.net:14003
    python ./src/app.py
    
The exporter was tested with python 3.10, but might also work with other versions.

### Limitations
Currently, it is recommended to only run one instance of the exporter for one account. The one instance can query an unlimited number of nodes.
It might also work to have multiple exporters for one account, but this is not tested yet and might lead to unforeseen issues. 
