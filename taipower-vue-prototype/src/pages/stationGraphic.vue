<template>
    <div>
        <div class="navbar navbar-expand-lg navbar-light mb-2">
            <div class="w-100">
                <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <label>{{ $t(`stationGraphic.tabs['${pageMode}']`) }}</label>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav col-12 col-lg-6 flex-wrap" ref="my_navbar">
                        <li class="nav-item col-12 col-lg-6  my-lg-width text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'sld' && layout == 0}" @click="pageMode = 'sld'; layout = 0;">{{$t('stationGraphic.tabs.sld')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-6 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'sld' && layout == 1}" @click="pageMode = 'sld'; layout = 1;">{{$t('stationGraphic.tabs.sld_layout')}}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <sld v-if="pageMode == 'sld'" :layout="layout"></sld>
    </div>
</template>

<script>
import sld from '@/components/stationGraphic/sld.vue'

export default {
    name: "stationGraphic",
    data(){
        return {
            pageMode: "sld",
            layout: 0, // For SLD
        }
    },
    components: {
        sld,
    }
}
</script>
