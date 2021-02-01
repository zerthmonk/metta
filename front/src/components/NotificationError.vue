<script>
export default {
  props: {
    message: {
      type: String,
    },
  },

  template: '<div class="notification notification_error">{{message}}</div>'
}
</script>

<style lang="sass" scoped>
  @import '../assets/variables'

  .notification_error
    font-weight: bold
    color: $danger
    border-color: $danger


</style>
