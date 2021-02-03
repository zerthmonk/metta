<template>
  <div class="user-login">
    <div class="user-login__wrapper" v-if="user">
      <user-stat :user=user :text=text></user-stat>
    </div>
    <p v-else>waiting for telegram connect...</p>
  </div>
</template>

<script>
import UserStat from './UserStat.vue';

export default {
  extends: UserStat,
  components: { UserStat },

  props: {
    text: {
      type: String,
      default: 'control account logged as'
    }
  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/variables'

  .user-login__wrapper
    display: flex
    justify-content: flex-start
</style>
