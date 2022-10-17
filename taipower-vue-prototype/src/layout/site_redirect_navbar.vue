<template>
    <nav class="navbar navbar-expand-lg navbar-light site_redirect_navbar p-0" v-if="Array.isArray(urlData) && urlData.length > 0">
        <div class="container-fluid p-0">
            <button class="navbar-toggler btn-outline-secondary m-2 ms-auto" type="button" data-bs-toggle="collapse" data-bs-target="#siteRedirectNav" aria-controls="siteRedirectNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon text-light"></span>
            </button>
            <div class="collapse navbar-collapse" id="siteRedirectNav">
                <ul class="navbar-nav" ref="navbar-nav">
                    <li class="nav-item" v-for="data in get_show_data" :key="data.name">
                        <a 
                            class="nav-link ps-4 pe-4" aria-current="page" :href="data.url"
                            :class="{'active': data.url == '#'}"
                        >
                            {{$store.state.language in data.name_i18n? data.name_i18n[$store.state.language] : data.name }}
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: "siteRedirectNavbar",
    props: {
        urlData: {
            type: Array,
            default: ()=>{
                return []
            }
        }
    },
    emits: ['nav-show'],
    computed: {
        get_show_data(){
            let showData = this.urlData.filter(i=>  'name' in i && 'route' in i && 'pageType' in i ? true : i.pageType == 'all'? true : i.pageType.includes(this.$store.state.user_data.pageType) )
            if(showData.length >0){
                this.$emit('nav-show')
            }
            return showData
        }
    }
}
</script>