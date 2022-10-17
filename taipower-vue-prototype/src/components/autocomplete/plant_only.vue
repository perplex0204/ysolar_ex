<template>
    <div>
        <el-autocomplete
            class="w-100"
            size="large"
            v-model="plant_search"
            :fetch-suggestions="querySearchAsync"
            :placeholder="$t('搜尋案場')"
            value-key="name"
            @select="handleSelect"
            :clearable="true"
            :teleported="false"
        ></el-autocomplete>
    </div>
</template>

<script>
export default {
    name: "AllType",
    data(){
        return {
            plant_search: "",
        }
    },
    emits: ['station-select', 'search-select'],
    props: {
        preSelect: {
            type: Boolean,
            default: false,
        }
    },
    methods: {
        async querySearchAsync(queryString, cb) {
			//console.log(queryString)
			//console.log(this.PV_data)
            await this.axios.post('/station_search_regex_plant', {
                query: queryString
            }).then(data => {
                //console.log(data.data.data)
                if(data.data.data.length == 0){
                    cb([{'name':  this.$i18n.t('無資料')}])
                }else{
                    cb(data.data.data)
                }
            })
			
		},
		handleSelect(item) {
			//console.log(item)
			if(item.name == this.$i18n.t('無資料')){
				return false
			}
            else{
                this.$emit('station-select', item)
            }

		},
    },
    mounted(){
        this.querySearchAsync('', (data)=>{
            if(!this.preSelect)
                return false
            for(var i in data){
                this.plant_search = data[i].name
                this.handleSelect(data[i])
                break
            }
            return false
        })
    },
    watch: {
        plant_search() {
            this.$emit('search-select', this.plant_search)
        }
    }
}
</script>