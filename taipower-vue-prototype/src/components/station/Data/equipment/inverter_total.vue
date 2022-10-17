<template>
    <div>
        <div class="ps-lg-4 pe-lg-4 d-flex justify-content-center">
            <div class="table-responsive w-100">
                <table class="table table-striped table-borderless text-center">
                    <thead>
                        <tr class="text-primary">
                            <th scope="col">{{$t('datatype.設備名稱')}}</th>
                            <th scope="col">{{$t('datatype.裝置容量')}} kW</th>
                            <th scope="col">{{$t('datatype.直流功率')}} kW</th>
                            <th scope="col">{{$t('datatype.交流功率')}} kW</th>
                            <th scope="col">{{$t('datatype.發電量')}} kWh</th>
                            <th scope="col">{{$t('datatype.Ambient溫度')}} °C</th>
                            <th scope="col">{{$t('datatype.變流器溫度')}} °C</th>
                            <th scope="col">{{$t('datatype.Boost溫度')}} °C</th>
                            <th scope="col">RA %</th>
                            <th scope="col">PR %</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="data in inv_total_data" :key="data.ID" @dblclick="row_click(data)">
                            <td class="text-success">{{data.name}}</td>
                            <td>{{data.capacity}}</td>
                            <td>{{data.p_cell_total}}</td>
                            <td>{{data.p_bus_total}}</td>
                            <td>{{data.kwh_today}}</td>
                            <td>{{data.temp_inner == undefined ? '---' : data.temp_inner}}</td>
                            <td>{{data.temp_sink == undefined ? '---' : data.temp_sink}}</td>
                            <td>{{data.temp_Boost_1 == undefined ? '---' : data.temp_Boost_1}}</td>
                            <td>{{data.RA}}</td>
                            <td>{{data.PR}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "inverterTotalTable",
    emits: ['update-parent-btn-name'],
    props: {
        inverterList: {
            type: Array,
            required: true
        }
    },
    data(){
        return {
            ID_list: [],
            inv_total_data: []
        }
    },
    methods: {
        pv_inv_total_data(){
            this.axios.post('/pv_inv_total_data', {
                ID_list: this.ID_list
            }).then(data => {
                console.log(data.data.data)
                this.inv_total_data = data.data.data
            })
        },
        row_click(data){
            console.log(data)
            this.inverterList.forEach(inv => {
                if(inv.ID == data.ID){
                    let obj = inv
                    obj['type'] = 'inv'
                    this.$emit('update-parent-btn-name', obj)
                }
            })
        }
    },
    mounted(){
        this.inverterList.forEach(inv => {
            this.ID_list.push(inv.ID)
        })
        this.pv_inv_total_data()
        this.sync_data = window.setInterval(this.pv_inv_total_data, 5000)
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    }
}
</script>
<style scoped>
.table > thead > tr > th{
    padding-top: 1rem;
    padding-bottom: 1rem;
}
.table > tbody > tr > td{
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>