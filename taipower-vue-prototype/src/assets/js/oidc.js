import Oidc from 'oidc-client'

export const vueBase = window.location.origin
// google
export const googleBase = 'http://accounts.google.com'
// export const googleClientId = '515379922335-6o2rdu1248ch932f4jj4j4qt6o5uovs4.apps.googleusercontent.com'
export const googleClientId = process.env.VUE_APP_OIDC_GOOGLE_CLIENT_ID


// github
export const githubBase = 'http://github.com/login/oauth/authorize'
// export const githubClientId = '00a9aa4e51a18e9a9367'
// export const githubClientSecret = 'fbd5d1527a2e08dafbd2db30f608bf712a4b8f57'
export const githubClientId = process.env.VUE_APP_OIDC_GITHUB_CLIENT_ID
export const githubClientSecret = process.env.VUE_APP_OIDC_GITHUB_CLIENT_SECRET


// gitlab
export const gitlabBase = 'https://gitlab.com'
// export const gitlabClientId = 'd398fbb7ff1e4708e9788a165b4db5f9a934f1806450a18ecb7cac4aa7f16bd0'
// export const gitlabClientSecret = '19e4dd47f1c2b53d726d0144c157e7bdb36df14ec402549b13b146e9d91c2051'
export const gitlabClientId = process.env.VUE_APP_OIDC_GITLAB_CLIENT_ID 
export const gitlabClientSecret = process.env.VUE_APP_OIDC_GITLAB_CLIENT_SECRET



export const googleOpenIdConnectSetting = {
    userStore: new Oidc.WebStorageStateStore(),
    authority: googleBase,
    client_id: googleClientId,
    redirect_uri: vueBase+'/openid_connect',
    post_logout_redirect_uri: vueBase,
    scope: 'openid profile address email',
    response_type: 'id_token token',
    loadUserInfo: true
}

export const githubOpenIdConnectSetting = {
    userStore: new Oidc.WebStorageStateStore(),
    authority: githubBase,
    client_id: githubClientId,
    client_secret: githubClientSecret,
    redirect_uri: vueBase+'/openid_connect',
    post_logout_redirect_uri: vueBase,
    scope: 'openid profile address email',
    response_type: 'id_token token',
    loadUserInfo: true,
    metadata: {
        issuer: githubBase,
        authorization_endpoint: githubBase
    }
}

export const gitlabOpenIdConnectSetting = {
    userStore: new Oidc.WebStorageStateStore(),
    authority: gitlabBase+"/oauth/authorize",
    client_id: gitlabClientId,
    client_secret: gitlabClientSecret,
    redirect_uri: vueBase+'/openid_connect',
    post_logout_redirect_uri: vueBase,
    scope: 'openid profile email',
    response_type: 'code',
    loadUserInfo: true,
    metadata: {
        issuer: gitlabBase,
        authorization_endpoint: gitlabBase+"/oauth/authorize",
        userinfo_endpoint: gitlabBase+"/oauth/userinfo",
        jwks_uri: gitlabBase+"/oauth/discovery/keys",
        token_endpoint: gitlabBase+"/oauth/token"
    }
}