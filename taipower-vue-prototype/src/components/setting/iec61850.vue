<template>
    <div>
        <iec61850-setting :commandList="commandList"></iec61850-setting>
    </div>
</template>
<script>
import iec61850Setting from './iec61850/iec61850_setting.vue'
export default {
    name: "iec61850",
    components: {
        iec61850Setting
    },
    data(){
        return {
            commandList: []
        }
    },
    mounted(){
        this.axios.post('/setting/get_IEC61850_parameter',{
                type: "GET"
            }).then(data=>{
                console.log(data.data.data)
                this.commandList = data.data.data
            })
    }
}
</script>
