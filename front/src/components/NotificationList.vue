<template>
  <div class="notification-wrapper">
    <NotificationError
      v-for="(text, key) in errors"
      :key="key"
      :message="text"
      />

    <NotificationInfo
      v-for="(text, key) in info"
      :key="key"
      :message="text"
      />

  </div>
</template>

<script>
import { getUniqueId } from '../helpers';
import { MESSAGE_TYPE_ALLOWED } from '../conf';
import NotificationError from './NotificationError.vue';
import NotificationInfo from './NotificationInfo.vue';

export default {

  data() {
    return {
      messages: {},
    }
  },

  props: {
    timeout: {
      type: Number,
      default: 4000
    },
    limit: {
      type: Number,
      default: 10
    }
  },

  components: {
    NotificationInfo,
    NotificationError
  },

  computed: {
    info() { return this.assignMessage(this.messages, 'info') },
    errors() { return this.assignMessage(this.messages, 'error') }
  },

  methods: {

    addMessage(type, text) {
      let _id = getUniqueId();
      // possibility of duplicate IDs is extremely low, though
      if (this.messages[_id]) _id = getUniqueId();
      if (!Object.values(MESSAGE_TYPE_ALLOWED).includes(type)) type = MESSAGE_TYPE_ALLOWED.default;

      const message = {
        id: _id,
        type: type,
        text: text,
      }
      // reactivity was learned the painful way
      const messageList = Object.values(this.messages);
      if (messageList.length >= this.limit) {
        const oldest = messageList[0];
        console.log(oldest);
        if (oldest) this.delMessage(oldest);
      }
      if (!message.infinite) {
        setTimeout(() => this.delMessage(message), this.timeout);
      }
      this.$set(this.messages, _id, message);
    },

    assignMessage(messages, messageType) {
      return Object.values(messages).reduce((accum, message) => {
        if (message.type === messageType) {
          accum[message.id] = `${messageType.toUpperCase()}: ${message.text}`;
        }
        return accum;
      }, {});
    },

    delMessage(message) {
      this.$delete(this.messages, message.id);
    },
  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/mixins';

  .notification-wrapper
    position: absolute
    bottom: 0
    right: 0
    min-width: 10vw
    max-width: 50vw
    margin: 1rem
    padding: 1rem

  .notification
    padding: .875rem
    margin: 2px;
    font-family: monospace
    background: rgba(0,0,0,0.8)
    border-left: 3px solid black;
    @include border-radius(5px)

</style>
