<script>
export default {
  props: {
    message: {
      type: String,
    },
  },
  template: '<div class="notification notification_info">{{message}}</div>'
}
</script>

<style lang="sass" scoped>
  @import '../assets/variables'

  .notification_info
    color: $main-light
    border-color: $main-normal

</style>
