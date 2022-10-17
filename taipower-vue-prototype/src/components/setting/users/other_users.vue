<template>
    <div class="mt-3">
        <div class="card p-4">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fa-users text-primary me-2"></i>{{$t('setting.users.使用者列表')}}</h5>
                <button class="btn btn-warning ms-auto col-12 col-lg-auto"
                @click="new_user()"
                data-bs-toggle="tooltip" data-bs-placement="bottom" :title="$t('setting.users.新增使用者')">
                    <i class="fa-solid fa-user-plus"></i>
                    <div class="d-inline d-lg-none">
                        {{$t('setting.users.新增使用者')}}
                    </div>
                </button>
            </div>
            <user-table class="mt-2" :tableData="table_data" :currentPage="current_page" :totalPage="total_page"
            @page-change="(new_page)=>{
              current_page = new_page  
              get_all_users_data()
            }"
            @reload-table="get_all_users_data" @update-user-data="update_user_data">
            </user-table>
        </div>
        <new-user-modal ref="new_user_modal" @reload-table="get_all_users_data"></new-user-modal>
    </div>
</template>
<script>
import userTable from './users_table.vue'
import newUserModal from './new_user_modal.vue' 

export default {
    name: "Other_users",
    components: {
        userTable,
        newUserModal
    },
    data(){
        return {
            table_data: [],
            current_page: 1,
            total_page: 1,
        }
    },
    methods: {
        get_all_users_data(){
            this.table_data = []
            this.axios.get(`/get_all_users_data?page=${this.current_page}`).then(data=>{
                this.table_data = data.data.data.users_list
                this.total_page = data.data.data.total_page
            })
        },
        update_user_data(ID, type, data){
            console.log(type, data)
            this.axios.post('/update_user_data', {
                ID: ID,
                mode: type,
                data: data
            }).catch(error => {console.error(error)})
        },
        new_user(){
            this.$refs.new_user_modal.open_modal()
        }
    },
    mounted(){
        this.get_all_users_data()
    }
}
</script>