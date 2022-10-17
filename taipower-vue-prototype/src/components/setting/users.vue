<template>
    <div>
        <users-card></users-card>
        <other-users v-if="$store.state.user_data.level >= 3"></other-users>
        <div style="min-height: 100px;"></div>
    </div>
</template>

<script>
import usersCard from './users/users_card.vue'
import otherUsers from './users/other_users.vue'

export default {
    name: "Users",
    components: {
        usersCard,
        otherUsers
    }
}
</script>

<style>

</style>