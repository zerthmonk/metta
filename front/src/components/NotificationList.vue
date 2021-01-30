<template>
  <div class="notification-wrapper">
    <ErrorNotification
      v-for="(text, key) in errors"
      :key="key"
      :message="text"
      />
    <InfoNotification
      v-for="(text, key) in info"
      :key="key"
      :message="text"
      />
  </div>
</template>

<script>
import ErrorNotification from './ErrorNotification.vue';

export default {

  props: {
    timeout: {
      type: Number,
      default: 500
    },
    messages: {
      type: Object,
    },
  },

  components: {
    ErrorNotification
  },

  computed: {
    info() { return this.setMessage(this.messages, 'info') },
    errors() { return this.setMessage(this.messages, 'error') }
  },

  methods: {
    setMessage: (messages, messageType) => {
      return Object.values(messages).reduce((accum, message) => {
        if (message.type === messageType) {
          accum[message.id] = `${messageType.toUpperCase()}: ${message.text}`;
        }
        return accum;
      }, {});
    }
  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/mixins';

  .notification-wrapper
    position: absolute
    margin: 1rem
    padding: 1rem
    top: 0
    right: 0
    min-width: 10vw
    max-width: 30vw

  .notification
    padding: .875rem
    font-family: monospace
    background: rgba(0,0,0,0.5)
    border-left: 3px solid black;
    @include border-radius(5px)


</style>
