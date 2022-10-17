<template>
    <div>
        <site-redirect-navbar-setting v-if="$store.state.user_data.is_superuser"></site-redirect-navbar-setting>
        <web-nav-page-card v-if="$store.state.user_data.is_superuser"></web-nav-page-card>
    </div>
</template>

<script>
import siteRedirectNavbarSetting from './web_nav_page/site_redirect_navbar_setting.vue'
import webNavPageCard from './web_nav_page/web_nav_page_card.vue'

export default {
    name: "webNavPage",
    components: {
        webNavPageCard,
        siteRedirectNavbarSetting
    }
}
</script>
