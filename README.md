# synology-ddns
[![Github](https://img.shields.io/badge/Github-100000.svg?logo=github&logoColor=white)](https://github.com/ChowRex/synology-ddns) ![Python](https://img.shields.io/badge/Python-14354C.svg?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000.svg?logo=flask&logoColor=white) [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/chowrex/synology-ddns) [![codecov](https://codecov.io/gh/ChowRex/synology-ddns/graph/badge.svg?token=o4k0DRXLnv)](https://codecov.io/gh/ChowRex/synology-ddns)

Synology DSM DDNS, custom DDNS provider

## How to use

<div style="
  position: relative;
  padding: 15px 15px 15px 45px;
  margin: 20px 0;
  border-left: 4px solid #ff9800;
  background-color: #fff8e6;
  border-radius: 0 5px 5px 0;
">
  <div style="
    position: absolute;
    left: 15px;
    top: 15px;
    font-size: 20px;
  ">⚠️</div>
  <strong>Warnning:</strong> It is highly recommended to use a valid certificate issued by <strong>Let's Encrypt</strong> or other authorities.
</div>

### Ensure that an SSL certificate has been added

<div style="
  position: relative;
  padding: 15px 15px 15px 45px;
  margin: 20px 0;
  border-left: 4px solid #5bc0de;
  background-color: #d9edf7;
  border-radius: 0 5px 5px 0;
">
   <div style="
    position: absolute;
    left: 15px;
    top: 15px;
    font-size: 20px;
  ">ℹ️</div>
  <strong>Skip tip:</strong> If you already have an SSL certificate, you can skip this section.
</div>

<details><summary>Click here for details</summary>

#### Create a self-signed certificate and download

1. Open `Contorl Panel` application ➡️ `Task Scheduler` ➡️ `Create` ➡️ `Scheduled Task`➡️ `User-definded script`

    ![CreateAnScheduledTask](synology_ddns/static/image/CreateAnScheduledTask.png)

2. Go to `Task Settings` ➡️  Input the script below, then click `OK`

    ![SetTaskSettings](synology_ddns/static/image/SetTaskSettings.png)

    You can replace `example.com` with any domain name you like, but be careful to comply with the domain specification ([RFC 1035: Domain names - implementation and specification](https://www.rfc-editor.org/rfc/rfc1035)).

    ```bash
    openssl req -x509 -newkey ec \
      -pkeyopt ec_paramgen_curve:prime256v1 \
      -keyout ecc.key -out ecc.crt \
      -days 365 -nodes -sha256 \
      -subj "/CN=exmaple.com"
    ```

3. Select the task you just added, then click `Run` button

    ![RunTheTask](synology_ddns/static/image/RunTheTask.png)

4. Open `File Station` application ➡️ `home` ➡️ Download the `eco.key` and `ecc.crt`

    ![DownloadSSLCertificate](synology_ddns/static/image/DownloadSSLCertificate.png)

#### Add the cretificate into DSM

1. Open `Contorl Panel` application ➡️ `Security` ➡️ `Certificate` ➡️ `Add`➡️ `Next`

    ![AddANewCertificate](synology_ddns/static/image/AddANewCertificate.png)

2. Input the certificate name then click `Next`

    ![InputCertificateName](synology_ddns/static/image/InputCertificateName.png)

3. Browse your key and certificate, then click `OK`

    ![BrowserAndUploadCertificate](synology_ddns/static/image/BrowserAndUploadCertificate.png)

</details>

### Set up service

#### 🐳 With `Docker`

<details><summary>Click here for details</summary>

##### Install and enable [Container Manager](https://www.synology.com/en-us/dsm/packages/ContainerManager) on your Synology DSM


1. Login your DSM then open `Package Center` application ➡️ Search bar input `container manager` ➡️ Get in `Container Manager` application.

    ![InstallContainerManager](synology_ddns/static/image/InstallContainerManager.png)

2. If you've installed this package, make it stay in `Running`status, if not, install it then keep it run.

    ![MakeContainerManagerRunning](synology_ddns/static/image/MakeContainerManagerRunning.png)

##### Pull image

1. Open `Container Manager` application, navigate to `Registry` section, search keyword `chowrex` ➡️ `chowrex/synology-ddns` ➡️ `Download`.

    ![FindOutDockerImage](synology_ddns/static/image/FindOutDockerImage.png)

2. Use `latest` tag, click `Download`.

    ![UseLatestDockerImageTag](synology_ddns/static/image/UseLatestDockerImageTag.png)

##### Run container

1. Goto `Image`, select the image just downloaded, click `Run`.

    ![RunDockerImage](synology_ddns/static/image/RunDockerImage.png)

2. Check `Enable auto-restart` checkbox, then click `Next` button.

    ![EnableAutoRestart](synology_ddns/static/image/EnableAutoRestart.png)

3. Set the local port to `5678` *(Or any number  between 1024 - 65535, if the port you specify has been taken, change another one)*,  then click `Next` button.

    ![SetContainerLocalPort](synology_ddns/static/image/SetContainerLocalPort.png)

4. Overview all settings and click `Done` button.

    ![OverviewAllContainerSettings](synology_ddns/static/image/OverviewAllContainerSettings.png)

5. After wait for a while, click the container name *(Here is `chowrex-synology-ddns-1` )* to enter the detail of container.

    ![EnterContainerDetail](synology_ddns/static/image/EnterContainerDetail.png)

6. Click the `Log` tab to see all logs, if everything is OK, some info logs will appear.

    ![ContainerInfoLogs](synology_ddns/static/image/ContainerInfoLogs.png)

##### Create a reverse proxy

1. Open `Contorl Panel` application ➡️ `Login Portal` ➡️ `Advanced` ➡️ `Reverse Proxy`

    ![OpenReverseProxySettings](synology_ddns/static/image/OpenReverseProxySettings.png)

2. Click `Create`

    ![CreateANewReverseProxy](synology_ddns/static/image/CreateANewReverseProxy.png)

3. Fill the `General` settings then click `Save`

    ![FillGeneralReverseProxySettings](synology_ddns/static/image/FillGeneralReverseProxySettings.png)

</details>

#### 🌐 With `Web Station`

<details><summary>Click here for details</summary>

##### Install and enable [Web Station](https://www.synology.com/en-us/dsm/packages/WebStation) on your Synology DSM


1. Login your DSM then open `Package Center` application ➡️ Search bar input `web station` ➡️ Get in `Web Station` application.

    ![FindOutWebStation](synology_ddns/static/image/FindOutWebStation.png)

2. If you've installed this package, make it stay in `Running`status, if not, install it then keep it run.

    ![MakeSureWebStationIsRunning](synology_ddns/static/image/MakeSureWebStationIsRunning.png)

##### Install and enable [Python 3.9 ](https://www.synology.com/en-us/dsm/packages/Python3.9)on your Synology DSM

Follow the same path, install `Python 3.9` and make it stay in `Running` status.

![InstallPython39](synology_ddns/static/image/InstallPython39.png)

![MakePython39Running](synology_ddns/static/image/MakePython39Running.png)

##### Copy this repository code into your web directory

1. Open `File Station` application, navigate to `web` directory, click `Create` ➡️ `Create folder`.

    ![CreateANewFolder](synology_ddns/static/image/CreateANewFolder.png)

2. Enter name then click `OK`.

    ![InputFolderName](synology_ddns/static/image/InputFolderName.png)

3. Navigate into the new folder, click `Upload` ➡️ `Upload - Skip`, upload all the files.

    ![UploadAllCode](synology_ddns/static/image/UploadAllCode.png)

##### Create a Python profile

1. Open `Web Station` application, Click `Script Language Settings` ➡️ `Python` ➡️ `Create`.

    ![CreateAPythonService](synology_ddns/static/image/CreateAPythonService.png)

2. Input `Profile Name` & `Description`, then click `Next`.

    - Profile Name: *DDNS*
    - Description: *Use for network DDNS*

    ![InputProfileNameAndDescription](synology_ddns/static/image/InputProfileNameAndDescription.png)

3. Set `Process` to `1`, `Max.request count` to `1024`, then click `Next`.

    ![SetProcessAndMaxRequestCount](synology_ddns/static/image/SetProcessAndMaxRequestCount.png)

4. Click `Browse` button to select the `requirements.txt` file, then click `Next` button.

    ![ClickBrowseButton](synology_ddns/static/image/ClickBrowseButton.png)

    ![SelectRequirementsFile](synology_ddns/static/image/SelectRequirementsFile.png)

    ![ClickNextButton](synology_ddns/static/image/ClickNextButton.png)

5. Overview all settings and click `Create` button.

    ![ClickCreateButtonForPython](synology_ddns/static/image/ClickCreateButtonForPython.png)

##### Create a Web service

1. Open `Web Station` application, Click `Web Service` ➡️ `Create`.

    ![CreateAWebService](synology_ddns/static/image/CreateAWebService.png)

2. Select `Native script language website` ➡️ `Python 3.9` ➡️ `DDNS`, then click `Next`.

    ![SelectPythonService](synology_ddns/static/image/SelectPythonService.png)

3. Input `Name`/`Description`, then select the correct `Document root` and `WSGI file`, click `Next`.

    - Name: *ddns-service*
    - Description: *Use for network DDNS*

    ![ConfirmGeneralSettings](synology_ddns/static/image/ConfirmGeneralSettings.png)

4. Overview all settings and click `Create` button.

    ![ClickCreateButtonForService](synology_ddns/static/image/ClickCreateButtonForService.png)

##### Create a Web portal

1. Open `Web Station` application, Click `Web Portal` ➡️ `Create`.

    ![CreateAWebPortal](synology_ddns/static/image/CreateAWebPortal.png)

2. Select `Web service portal` type as new portal.

    ![SelectWebServicePortal](synology_ddns/static/image/SelectWebServicePortal.png)

3. Set up web service portal detail, **MUST** use `Name-based` type, cause the Synology ***DO NOT*** accept plain HTTP request.

    ![SelectPortalDetails](synology_ddns/static/image/SelectPortalDetails.png)

</details>

### Verify service

#### Have an owned private DNS server

<details><summary>Click here for details</summary>

Add your service FQDN into your own DNS server. The following is a sample configuration of the `named` service.

```bash
$TTL    604800
@       IN      SOA     ns1.example.com. admin.example.com. (
                             2023010101         ; Serial
                             604800            ; Refresh
                             86400             ; Retry
                             2419200           ; Expire
                             604800 )          ; Negative Cache TTL
;
@       IN      NS      ns1.example.com.
ns1     IN      A       192.168.1.100 ; Your DSM IP address
ddns    IN      A       192.168.1.100 ; Your DSM IP address
```

</details>

#### Use Synology DNS Server

<details><summary>Click here for details</summary>

##### Install and enable [DNS Server](https://www.synology.com/en-us/dsm/packages/DNSServer) on your Synology DSM


1. Login your DSM then open `Package Center` application ➡️ Search bar input `dns server` ➡️ Get in `DNS Server` application.

    ![InstallDNSServer](synology_ddns/static/image/InstallDNSServer.png)

2. If you've installed this package, make it stay in `Running`status, if not, install it then keep it run.

    ![MakeDNSServerRunning](synology_ddns/static/image/MakeDNSServerRunning.png)

##### Create the specify zone

1. Open `DNS Server` application ➡️ `Zones` ➡️ `Create` ➡️ `Primary zone`.

    ![CreateANewPrimaryZone](synology_ddns/static/image/CreateANewPrimaryZone.png)

2. Specify the basic info, then click `Save` button.

    - Domain name: *example.com*
    - Primary DNS server: *8.8.8.8*

    ![FillZoneSettings](synology_ddns/static/image/FillZoneSettings.png)

3. Choose the zone, then click `Edit` ➡️ `Resource record`

    ![ModifyRecords](synology_ddns/static/image/ModifyRecords.png)

4. Click `Create` ➡️ `A Type`

    ![CreateANewARecord](synology_ddns/static/image/CreateANewARecord.png)

5. Fill the record info, then click `Save` button. 

    - Name: *ddns*
    - IP address: *YOUR DSM IP ADDRESS*

    ![FillRecordSettings](synology_ddns/static/image/FillRecordSettings.png)

</details>

#### Verify

<details><summary>Click here for details</summary>

##### Before you go

Make sure:

- Your DSM's DNS setting has already pointed to your DNS server.

    ![DSMDNSSettings](synology_ddns/static/image/DSMDNSSettings.png)

- Your computer's DNS setting has already pointed to your DNS server, see: [Get Started  |  Public DNS  |  Google for Developers](https://developers.google.com/speed/public-dns/docs/using)

##### Do verify

1. Use your browser to visit the service page, for common scenarios, try: https://ddns.example.com
2. If everything is OK, the website will show this document.

</details>

### Configure System DDNS

<details><summary>Click here to show</summary>

1. Open `Contorl Panel` application ➡️ `External Access` ➡️ `DDNS` ➡️ `Add`

    ![AddADDNSProvider](synology_ddns/static/image/AddADDNSProvider.png)

2. Click the `Customize Provider` button to create a new one.

    ![ChoseProviderAndRule](synology_ddns/static/image/CreateCustomizeProvider.png)

3. Click `Add` button, then input `Service Provider`&`Query URL`, then click `Save` button.

    - Service Provider: *CloudFlare*
    - Webhook URL: *https://ddns.example.com/?api=cloud_flare&hostname=__HOSTNAME__&myip=__MYIP__&username=__USERNAME__&password=__PASSWORD__*

    ![CreateANewDDNSProvider](synology_ddns/static/image/CreateANewDDNSProvider.png)

4. Set `Service Provider` to `CloudFlare`, then input the key info.

    - Hostname: *Address-of.your-own-zone.com*
    - Username: *your-own-zone.com*
    - Password: *The user token of your CloudFlare account*
    
    ![AddADDNSService](synology_ddns/static/image/AddADDNSService.png)
    
5. If click `Test Connection` returns `Normal`, then click `OK` button & done 🎉

</details>

## Design Ideas

<details><summary>Click here for details</summary>

### Digging into constraints and the operating principles behind

#### Official document

Let's start with Synology's criteria for customising DDNS providers.

> [DDNS | DSM - Synology Knowledge Center](https://kb.synology.com/en-global/DSM/help/DSM/AdminCenter/connection_ddns?version=7#b_23)

As mentioned above, a typical standard query URL would look like this: 

```http

https://Custom-DDNS-Provider.domain.com?HOSTNAME=__HOSTNAME__&MYIP=__MYIP__&USERNAME=__USERNAME__&PASSWORD=__PASSWORD__&PARAM1=value1&PARAM2=Value2
```

#### Official configuration

We can find some useful information from the `/etc/ddns_provider.conf`

> Input:
> 
>   1. DynDNS style request:
> 
>      modulepath = DynDNS
> 
>      queryurl = [Update URL]?[Query Parameters]
>
>   2. Self-defined module:
> 
>      modulepath = /sbin/xxxddns
> 
>      queryurl = DDNS_Provider_Name
>
> Our service will assign parameters in the following order when calling module:
> 
> (\$1=username, \$2=password, \$3=hostname, \$4=ip)
>
> Output:
> 
> When you write your own module, you can use the following words to tell user what happen by print it.
> 
> You can use your own message, but there is no multiple-language support.
>
> - good -  Update successfully.
> - nochg - Update successfully but the IP address have not changed.
> - nohost - The hostname specified does not exist in this user account.
> - abuse - The hostname specified is blocked for update abuse.
> - notfqdn - The hostname specified is not a fully-qualified domain name.
> - badauth - Authenticate failed.
> - 911 - There is a problem or scheduled maintenance on provider side
> - badagent - The user agent sent bad request(like HTTP method/parameters is not permitted)
> - badresolv - Failed to connect to  because failed to resolve provider address.
> - badconn - Failed to connect to provider because connection timeout.
>
> ...
>
> [DYNDNS.org]
> 
> modulepath=DynDNS
> 
> queryurl=https://members.dyndns.org/nic/update?hostname=__HOSTNAME__&myip=__MYIP__&system=dyndns&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG
>
> ...

I've tried a few ways to understand exactly what's going on behind the scenes

1. When I try to access the `DynDNS`'s API endpoint without any query parameters(*https://members.dyndns.org/nic/update*), I got an error message: `badauth`

2. I have tried to add a custom provider from the DSM UI and after adding it I can see DSM's default configuration behaviour for custom providers via the `/etc/ddns_provider.conf` file

    ```ini
    [USER_TEST]
      queryurl=https://api.example.com?hostname=__HOSTNAME__&myip=__MYIP__&username=__USERNAME__&password=__PASSWORD__
      modulepath=DynDNS
    ```

    As you can see , the `DynDNS` is the default custom provider's module, although I didn't find it system-wide.

    However, I searched the official documentation for DynDNS and found some useful information

    > Source: [Perform Update (RA-API) | Dyn Help Center](https://help.dyn.com/remote-access-api/perform-update/)
    >
    > #### Raw HTTP GET Request
    >
    > Actual HTTP request should look like following fragment. Note that there is the **bare minimum** set of headers. Request should be followed by sending an empty line.
    >
    > Fragment **base-64-authorization** should be represented by Base 64 encoded **username:password** string.
    >
    > ```
    > GET /nic/update?hostname=yourhostname&myip=ipaddress&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG HTTP/1.0
    > Host: members.dyndns.org
    > Authorization: Basic base-64-authorization
    > User-Agent: Company - Device - Version Number
    > ```
    >
    > Please note that although POST requests are permitted and will be processed, we don’t encourage developers to use them. We might stop processing of POST requests at any time, without notice.

    From the above information we can conclude that the module DynDNS uses the `GET` method as a request and asks to pass the username and password, DSM automatically helps you to convert the username and password.

#### Summary

After analysis, here are the summary:

1. There are `4` important variables in a query URL

    | Parameter      | Description                                                               |
    |----------------|---------------------------------------------------------------------------|
    | `__HOSTNAME__` | Domain name used to refer to the address being updated for this operation |
    | `__MYIP__`     | Used to refer to the address updated by this operation                    |
    | `__USERNAME__` | Used to refer to the authentication account required for this operation   |
    | `__PASSWORD__` | Used to refer to the authentication password required for this operation  |

    At the same time, additional request parameters can be added, depending on the vendor.

2. The default behaviour for custom providers to update records is to use the `DynDNS` module and execute it via the `GET` method

3. There are `TWO` ways to implement a custom DDNS provider

    - Define your customer module and query URL (*Difficult and requires command line knowledge*)
    - Use the DSM UI to create a default custom DDNS provider(*Just use DynDNS module*) and then provide a custom request URL (*Simple and requires no specialised knowledge*)

4. The responses are strictly limited accordingly

    - good -  Update successfully.
    - nochg - Update successfully but the IP address have not changed.
    - nohost - The hostname specified does not exist in this user account.
    - abuse - The hostname specified is blocked for update abuse.
    - notfqdn - The hostname specified is not a fully-qualified domain name.
    - badauth - Authenticate failed.
    - 911 - There is a problem or scheduled maintenance on provider side
    - badagent - The user agent sent bad request(like HTTP method/parameters is not permitted)
    - badresolv - Failed to connect to  because failed to resolve provider address.
    - badconn - Failed to connect to provider because connection timeout.

### Assessment of needs

With the above understanding of the limitations and implementation rules for custom DDNS providers, the basic implementation requirements:

The simplest way to fulfil the requirement is to use the `GET` method, which **DOES NOT** support *headers* or *json* or other types of requests such as `POST`/`PUT`, and all the content of the request **CAN ONLY** be passed via *parameters*.

The parameters requirements are below

| Required | Parameter | PlaceHolder      | Comment                                                                                                   |
|----------|-----------|------------------|-----------------------------------------------------------------------------------------------------------|
| ✓        | api       | `None`           | Used to distinguish between different DDNS provider names                                                 |
| ✓        | myip      | \_\_MYIP\_\_     | Recorded value of the current dynamic IP address                                                          |
| ✗        | hostname  | \_\_HOSTNAME\_\_ | The name of the record set by the DNS provider, which can be obtained from an environment variable.       |
| ✗        | username  | \_\_USERNAME\_\_ | Username for DNS provider authentication use, which can be obtained from an environment variable or file. |
| ✗        | password  | \_\_PASSWORD\_\_ | Password for DNS provider authentication use, which can be obtained from an environment variable or file. |

By using the [python-dotenv](https://pypi.org/project/python-dotenv/) package, I think it's possible to maintain the simplicity and flexibility of the API interface while maintaining the confidentiality of confidential information.

### Summary

#### Conclude

- The API interface should only accept `GET` type requests
- The API interface can accept 5 parameters: **api**/**myip**/*hostname*/*username*/*password*, of which `api` and `myip` are required, other parameters must can be obtained from an environment variable or file.
- The API interface's response is strictly limited accordingly: *good* / *nochg* / *nohost* / *abuse* / *notfqdn* / *badauth* / *911* / *badagent* / *badresolv* / *badconn*

</details>

## Mindmap

### Framework

<details><summary>Click here to show</summary>

```mermaid
flowchart TD
    good
    nochg
    nohost
    abuse
    notfqdn
    badauth
    911
    badagent
    badresolv
    badconn
    
    User(("API User")) -->|GET| API_Interface{{"API Interface"}}
    API_Interface --> Check_api_myip{"Both api and myip are provided?"}
    Check_api_myip --> |"No"| Show_Doc["Show the document"]
    Check_api_myip --> |"Other"| Check_Variables{"Are all required variables provided?"}
    Check_Variables --> |"No"| badagent
    Check_Variables --> |"Yes"| Check_FQDN{"Does the hostname match the FQDN?"}
    Check_FQDN --> |"No"| notfqdn
    Check_FQDN --> |"Yes"| Check_Same_Record{"Does the myip not changed?"}
    Check_Same_Record --> |"Yes"| nochg
    Check_Same_Record --> |"No"| Resolve_Endpoint{"Does the API Endpoint resolved properly?"}
    Resolve_Endpoint --> |"No"| badresolv
    Resolve_Endpoint --> |"Yes"| API_Provider(["Custom DDNS Provider"])
    API_Provider --> |"GET/PUT/POST"| Get_Response_Code{"Is the return response status code OK?"}
    Get_Response_Code --> |"200"| good
    Get_Response_Code --> |"401"| badauth
    Get_Response_Code --> |"403"| abuse
    Get_Response_Code --> |"404"| nohost
    Get_Response_Code --> |"408"| badconn
    Get_Response_Code --> |"500"| 911
    Get_Response_Code --> |"Other"| Raise[["Raise exceptions"]]

```

</details>

### CloudFlare

<details><summary>Click here to show</summary>

```mermaid
flowchart TD

    subgraph "Reponses"
    good
    badauth
    nohost
    end

    subgraph "Can get valid client?"
    get_client_by_user{"`Can get client by _user_ token?`"}
    get_client_by_account{"`Can get client by _account_ token?`"}

    get_client_by_user --> |"Yes"| client(("CloudFlare Client"))
    get_client_by_account --> |"Yes"| client
    get_client_by_user --> |"No"| get_client_by_account
    get_client_by_account --> |"No"| badauth
    end

    subgraph "Can get valid zone id?"
    zone_id(("zone id"))
    Is_zone_id_cached{"`Is the zone id mapped to _username_ cached?`"}
    can_get_zone_id{"`Is it possible to get the correct zone id by _username_?`"}

    Is_zone_id_cached --> |"Yes"| zone_id
    Is_zone_id_cached --> |"No"| can_get_zone_id
    client -.-> can_get_zone_id

    can_get_zone_id --> |"Yes"| zone_id
    can_get_zone_id --> |"No"| nohost
    end

    subgraph "Can get valid record id?"
    record_id(("record id"))
    Is_hostname_cached{"`Is the record id mapped to _hostname_ cached?`"}
    
    Is_hostname_cached --> |"Yes"| record_id
    Is_hostname_cached --> |"No"| Is_zone_id_cached
    end

    subgraph "Determine the record"
    is_record_exists{"Is the record exists?"}
    client -.-> is_record_exists
    zone_id -.-> is_record_exists
    end

    subgraph "Edit record"
    is_update_success{"Is the update operation successful?"}
    is_record_exists --> |"Yes"| is_update_success
    record_id -.-> is_update_success
    client -.-> is_update_success
    is_update_success --> |"Yes"| good
    is_update_success --> |"No"| badauth
    end

    subgraph "Create record"
    is_create_success{"Is the create operation successful?"}
    is_record_exists --> |"No"| is_create_success
    zone_id -.-> is_create_success
    client -.-> is_create_success
    is_create_success --> |"Yes"| good
    is_create_success --> |"No"| badauth
    end

    Request(("API Request")) -->|call| CloudFlare{{"CloudFlare DDNS provider"}}
    CloudFlare --> Is_hostname_cached

```

</details>
