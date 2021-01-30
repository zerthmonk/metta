<template>
  <div v-if="user">
    <div class="user-photo">
    </div>
    <div class="user-info">
      <p>{{user.username}}</p>
      <p>{{user.first_name}} {{user.last_name}}</p>
    </div>
  </div>
  <p v-else>loading...</p>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      requested: true
    },
  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/variables'

  .user-photo
    background: beige
    max-width: 100px
    max-height: 100px
    border-radius: 50%

  p
    color: $main-normal;

</style>
