# taipower-vue

Photovoltaic Surveillance System Website

AUTHOR : YUSHAN

<br>

---
## Environment Variable
* Require means program won't run if variable missing.

Name                      | Description                                            | Require  | Default                         |
------------------------- | ------------------------------------------------------ | -------- | ------------------------------- |
VUE_APP_GOOGLE_API_KEY    | Google Maps Platform Credentials                       |         |                                 |
VUE_APP_OIDC_GOOGLE_CLIENT_ID    | client_id of google for open id connect                                     |       |  |
VUE_APP_OIDC_GITHUB_CLIENT_ID    | client_id of github for open id connect                                     |       |  |
VUE_APP_OIDC_GITHUB_CLIENT_SECRET| client_secret of github for open id connect                                 |       |  |
VUE_APP_OIDC_GITLAB_CLIENT_ID    | client_id of gitlab for open id connect ( gitlab should login as admin )    |       |  |
VUE_APP_OIDC_GITLAB_CLIENT_SECRET|client_secret of gitlab for open id connect ( gitlab should login as admin ) |       |  |

**How to Add Environment Variable?**

You can add env variables in .env file, there are serveral types of env files depend on different stage of project, like develop, build, etc.  
<br/>

***STRONGLY RECOMMEND*** to put credential variables inside .env.local which won't be tracked by git.

[Read more about environment variables in vue](https://cli.vuejs.org/guide/mode-and-env.html)

<br>

---
## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
