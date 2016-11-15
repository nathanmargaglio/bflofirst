import requests
s = requests.Session()
s.cookies['nyssplash'] = 'buffalo'
s.cookies['test'] = 'test'
s.cookies['_gat'] = '1'
s.cookies['_ga'] = 'GA1.2.1065857682.1478637792'
s.cookies['_gat_newTracker'] = '1'
s.cookies['_idp_authn_lc_key']='6301ae5a5ac7ff909b52ad8bf50326a84ed4618015c9a248403c907d1467f70e'
s.cookies['clareitysecurity']='ca5cb009f1f6ea65880bbf6b3d12cf8f71d6ced1'
s.cookies['clareitysecurity']='ca4201a04a2e97ca55e14fb9c0bdd9fc7d5d6f6e'

s.get("https://idp.mynysmls.com/idp/Authn/UserPassword").text
print s.cookies
r = s.post("https://idp.mynysmls.com/idp/Authn/UserPassword", 
                  data={'j_username': 'smithray', 'password': 'queen2016', 'j_password': 'queen2016', 'j_logintype': 'sso'})

r = s.post("https://idp.mynysmls.com/idp/profile/SAML2/POST/SSO", data={"SAMLRequest":"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c2FtbDJwOkF1dGhuUmVxdWVzdCB4bWxuczpzYW1sMnA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCIgQXNzZXJ0aW9uQ29uc3VtZXJTZXJ2aWNlVVJMPSJodHRwczovL3BvcnRhbC5teW55c21scy5jb20vc2FtbCIgRGVzdGluYXRpb249Imh0dHBzOi8vaWRwLm15bnlzbWxzLmNvbTo0NDMvaWRwL3Byb2ZpbGUvU0FNTDIvUE9TVC9TU08iIElEPSJfNjU2YTJjZjYtYzc0ZC00ZjY3LWI3ZWYtMmE5ZWE0ZTFhNzkzIiBJc3N1ZUluc3RhbnQ9IjIwMTYtMTEtMDhUMjA6NDk6NDEuODg3WiIgUHJvdG9jb2xCaW5kaW5nPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YmluZGluZ3M6SFRUUC1QT1NUIiBWZXJzaW9uPSIyLjAiPjxzYW1sMjpJc3N1ZXIgeG1sbnM6c2FtbDI9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iPmh0dHBzOi8vcG9ydGFsLm15bnlzbWxzLmNvbS9zYW1sL3NwPC9zYW1sMjpJc3N1ZXI+PG1kOkV4dGVuc2lvbnMgeG1sbnM6bWQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDptZXRhZGF0YSI+PHRocnB0eTpSZXNwb25kVG8geG1sbnM6dGhycHR5PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDpwcm90b2NvbDpleHQ6dGhpcmQtcGFydHkiPmh0dHBzOi8vcG9ydGFsLm15bnlzbWxzLmNvbS9zYW1sPC90aHJwdHk6UmVzcG9uZFRvPjwvbWQ6RXh0ZW5zaW9ucz48c2FtbDJwOk5hbWVJRFBvbGljeSBBbGxvd0NyZWF0ZT0idHJ1ZSIvPjwvc2FtbDJwOkF1dGhuUmVxdWVzdD4=",
                                                                        "RelayState":"cG9ydGFs"})

#r = s.post("https://portal.mynysmls.com/saml", data={"SAMLRequest":"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c2FtbDJwOkF1dGhuUmVxdWVzdCB4bWxuczpzYW1sMnA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCIgQXNzZXJ0aW9uQ29uc3VtZXJTZXJ2aWNlVVJMPSJodHRwczovL3BvcnRhbC5teW55c21scy5jb20vc2FtbCIgRGVzdGluYXRpb249Imh0dHBzOi8vaWRwLm15bnlzbWxzLmNvbTo0NDMvaWRwL3Byb2ZpbGUvU0FNTDIvUE9TVC9TU08iIElEPSJfNjU2YTJjZjYtYzc0ZC00ZjY3LWI3ZWYtMmE5ZWE0ZTFhNzkzIiBJc3N1ZUluc3RhbnQ9IjIwMTYtMTEtMDhUMjA6NDk6NDEuODg3WiIgUHJvdG9jb2xCaW5kaW5nPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YmluZGluZ3M6SFRUUC1QT1NUIiBWZXJzaW9uPSIyLjAiPjxzYW1sMjpJc3N1ZXIgeG1sbnM6c2FtbDI9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iPmh0dHBzOi8vcG9ydGFsLm15bnlzbWxzLmNvbS9zYW1sL3NwPC9zYW1sMjpJc3N1ZXI+PG1kOkV4dGVuc2lvbnMgeG1sbnM6bWQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDptZXRhZGF0YSI+PHRocnB0eTpSZXNwb25kVG8geG1sbnM6dGhycHR5PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDpwcm90b2NvbDpleHQ6dGhpcmQtcGFydHkiPmh0dHBzOi8vcG9ydGFsLm15bnlzbWxzLmNvbS9zYW1sPC90aHJwdHk6UmVzcG9uZFRvPjwvbWQ6RXh0ZW5zaW9ucz48c2FtbDJwOk5hbWVJRFBvbGljeSBBbGxvd0NyZWF0ZT0idHJ1ZSIvPjwvc2FtbDJwOkF1dGhuUmVxdWVzdD4=",
#                                                                        "RelayState":"cG9ydGFs"})
print(r.status_code, r.reason)
print r.text