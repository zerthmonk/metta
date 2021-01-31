<template>
  <div class="user-photo" :style=image></div>
</template>

<script>

const IMG = '/shared';

export default {
  props: {
    uid: {
      type: Number,
    },
    size: {
      type: String,
      default: '50px'
    }
  },

  computed: {
    image() {
      return `
        background-image: url("${IMG}/${this.uid}.jpg");
        width: ${this.size};
        height: ${this.size};
      `
    }
  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/mixins'

  .user-photo
    background: beige
    background: url({{uid}})
    background-size: contain
    @include border-radius(5px)

</style>
