<template>
  <div> <!-- for flex -->
    <div class="user-stat" v-if="user">
      <UserPhoto
        :uid="user.id"
        :size="size"
      />
      <div class="user-stat_info"
        :style="lineSize"
      >
        <span>{{text}} <a :href=link>@{{user.username}} ( {{user.first_name}} {{user.last_name}} )</a></span>
        <span></span>
      </div>
    </div>
  </div>
</template>

<script>
import UserPhoto from './UserPhoto.vue';

export default {
  props: {
    text: {
      type: String,
      default: 'user info:'
    },
    user: {
      type: Object,
      requested: true
    },
    size: {
      type: String,
      default: '60px'
    }
  },

  components: { UserPhoto },

  computed: {
    link() { return `https://t.me/${this.user.username}` },
    lineSize() { return `line-height: ${this.size};` }
  },
}
</script>

<style lang="sass">
  @import '../assets/variables'

  .user-stat
    color: $main-light;
    display: flex
    justify-content: space-between
    max-width: 100%
    width: auto
    font-family: monospace
    font-weight: 600
    letter-spacing: 1px
    text-transform: uppercase

  .user-stat_info
    margin-left: 2rem
    height: 100%

  a
    text-decoration: none

    &:hover
      color: darken($main-normal, 15%)

</style>
