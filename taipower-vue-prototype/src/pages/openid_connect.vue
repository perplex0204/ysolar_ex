<template>
    <div></div>
</template>

<script>
import Oidc from "oidc-client"
import { googleOpenIdConnectSetting, gitlabOpenIdConnectSetting } from "@/assets/js/oidc.js"
export default {
    name: "openid_connect",
    created(){
        let that = this
        let userManager = undefined
        console.log(localStorage.getItem("solar_vue_oidc"))
        if(localStorage.getItem("solar_vue_oidc") == 'gmail'){
            userManager = new Oidc.UserManager(googleOpenIdConnectSetting)
        }
        else if(localStorage.getItem("solar_vue_oidc") == 'github'){
            if(window.location.href.indexOf('code=') == -1){
                this.$router.push("/login")
            }
            else{
                var state = window.location.href.indexOf('&state')
                var str = window.location.href.substring(window.location.href.indexOf('code=')+5, state)
                var code = str.substring()
                var login_form = new FormData()
                login_form.append("oidc_type", "github")
                login_form.append("code", code)
                this.axios.post('oidc', login_form).then(data => {
                    that.$store.dispatch('get_navLink').then(()=>{
                        setTimeout(function(){
                            const next_route = localStorage.getItem('solar_vue_previous_route')
                            if(![null, '/login', '/logout', '/openid_connect'].includes(next_route)){
                                // redirect to previous page
                                localStorage.removeItem('solar_vue_previous_route')
                                that.$router.push(next_route)
                            }else{
                                that.$router.push('/')
                            }
                        }, 500)

                    }).catch(e => {
                        alert("Error")
                        this.$router.go()
                    })

                }).catch(function(e){
                    console.log(e)
                    that.$router.push("/login")
                })
            }
            return true
        }
        else if(localStorage.getItem("solar_vue_oidc") == 'gitlab'){
            userManager = new Oidc.UserManager(gitlabOpenIdConnectSetting)
        }
        userManager.signinRedirectCallback().then(() => {
            userManager.getUser().then((user) => {
                if(user){
                    // console.log(JSON.stringify(user))
                    var login_form = new FormData()
                    login_form.append("oidc_type", localStorage.getItem("solar_vue_oidc"))
                    login_form.append("id_token", JSON.stringify(user))
                    that.axios.post('oidc', login_form).then(data => {
                        that.$store.dispatch('get_navLink').then(()=>{
                            setTimeout(function(){
                                const next_route = localStorage.getItem('solar_vue_previous_route')
                                if(![null, '/login', '/logout', '/openid_connect'].includes(next_route)){
                                    // redirect to previous page
                                    localStorage.removeItem('solar_vue_previous_route')
                                    that.$router.push(next_route)
                                }else{
                                    that.$router.push('/')
                                }
                            }, 500)

                        }).catch(e => {
                            alert("Error")
                            this.$router.go()
                        })

                    }).catch(function(e){
                        console.warn(e)
                        that.$router.push("/login")
                    })
                }
                else{
                    that.$router.push("/login")  
                }
            })
        })
        .catch(function(e){
            console.log("CallBack error"+e)
            that.$router.push("/login")
        })
    },
}
</script>