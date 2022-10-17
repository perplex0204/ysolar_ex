<template>
    <div class="cover-page card">
        <div class="position-absolute top-50 start-50 translate-middle text-center">
            <img src="imgs/logo.png" width="200" />
            <h1 class="mt-2">{{$t('homePage.export_cover.太陽光電系統報表')}}</h1>
        </div>
        <div class="position-absolute bottom-0 start-50 translate-middle-x">
            <h6>{{$t('homePage.export_cover.製表時間')}}：{{current_date}}</h6>
        </div>
    </div>    
</template>
<script>
export default {
    name: "exportCover",
    computed:{
        current_date(){
            let yourDate = new Date()
            yourDate.toISOString().split('T')[0]
            const offset = yourDate.getTimezoneOffset()
            yourDate = new Date(yourDate.getTime() - (offset*60*1000))
            return yourDate.toISOString().split('T')[0]
        }
    },
    mounted(){
        this.$store.commit('setLang', this.$store.state.language)
    }
}
</script>
<style scoped>
.cover-page{
    width: 21cm;
    min-height: 100vh !important;
}
</style>