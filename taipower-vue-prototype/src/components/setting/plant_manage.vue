<template>
    <div>
        <fast-modify></fast-modify>
        <div v-if="$store.state.user_data.is_superuser"><equipment-record></equipment-record></div>
        <div>
            <equipment-manage></equipment-manage>
        </div>
    </div>
</template>

<script>
import fastModify from './plant_manage/fast_modify.vue'
import equipmentRecord from './plant_manage/equipment_record.vue'
import equipmentManage from './plant_manage/equipment_manage.vue'

export default {
    name: "plantManage",
    components: {
        fastModify,
        equipmentRecord,
        equipmentManage
    }
}
</script>