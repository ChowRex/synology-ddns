# synology-ddns
Synology DSM DDNS, custom DDNS provider

## Design Ideas

### Digging into constraints and the operating principles behind

#### Official document

Let's start with Synology's criteria for customising DDNS providers.

> [DDNS | DSM - Synology Knowledge Center](https://kb.synology.com/en-global/DSM/help/DSM/AdminCenter/connection_ddns?version=7#b_23)

As mentioned above, a typical standard query URL would look like this: 

```http

http(s)://Custom-DDNS-Provider.domain.com?HOSTNAME=__HOSTNAME__&MYIP=__MYIP__&USERNAME=__USERNAME__&PASSWORD=__PASSWORD__&PARAM1=value1&PARAM2=Value2
```

#### Official configuration

We can find some useful information from the `/etc/ddns_provider.conf`

>  Input:
>     1. DynDNS style request:
>        modulepath = DynDNS
>        queryurl = [Update URL]?[Query Parameters]
>
> 2. Self-defined module:
>      modulepath = /sbin/xxxddns
>      queryurl = DDNS_Provider_Name
>
>    Our service will assign parameters in the following order when calling module:
>        (\$1=username, \$2=password, \$3=hostname, \$4=ip)
>
>  Output:
>     When you write your own module, you can use the following words to tell user what happen by print it.
>     You can use your own message, but there is no multiple-language support.
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
>         modulepath=DynDNS
>         queryurl=https://members.dyndns.org/nic/update?hostname=__HOSTNAME__&myip=__MYIP__&system=dyndns&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG
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

    | Parameter      | Description                                                  |
    | -------------- | ------------------------------------------------------------ |
    | `__HOSTNAME__` | Domain name used to refer to the address being updated for this operation |
    | `__MYIP__`     | Used to refer to the address updated by this operation       |
    | `__USERNAME__` | Used to refer to the authentication account required for this operation |
    | `__PASSWORD__` | Used to refer to the authentication password required for this operation |

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

| Required | Parameter | PlaceHolder      | Comment                                                      |
| -------- | --------- | ---------------- | ------------------------------------------------------------ |
| ✓        | api       | `None`           | Used to distinguish between different DDNS provider names    |
| ✓        | myip      | \_\_MYIP\_\_     | Recorded value of the current dynamic IP address             |
| ✗        | hostname  | \_\_HOSTNAME\_\_ | The name of the record set by the DNS provider, which can be obtained from an environment variable. |
| ✗        | username  | \_\_USERNAME\_\_ | Username for DNS provider authentication use, which can be obtained from an environment variable or file. |
| ✗        | password  | \_\_PASSWORD\_\_ | Password for DNS provider authentication use, which can be obtained from an environment variable or file. |

By using the [python-dotenv](https://pypi.org/project/python-dotenv/) package, I think it's possible to maintain the simplicity and flexibility of the API interface while maintaining the confidentiality of confidential information.

### Summary

#### Conclude

- The API interface should only accept `GET` type requests
- The API interface can accept 5 parameters: **api**/**myip**/*hostname*/*username*/*password*, of which `api` and `myip` are required, other parameters must can be obtained from an environment variable or file.
- The API interface's response is strictly limited accordingly: *good* / *nochg* / *nohost* / *abuse* / *notfqdn* / *badauth* / *911* / *badagent* / *badresolv* / *badconn*

#### Mindmap

##### Framework

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

##### CloudFlare

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

