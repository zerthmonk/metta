<template>
  <div id="app" class="container">
    <div class="content user-content">
      <UserStat
        :user="user"
      />
    </div>
    <NotificationList
      :messages="messages"
      />
  </div>
</template>

<script>
import axios from 'axios';
import UserStat from './components/UserStat.vue';
import NotificationList from './components/NotificationList.vue';
import { getUniqueId } from './helpers';

const messageTypeAllowed = ['info', 'error'];

export default {
  name: 'app',
  components: {
    UserStat,
    NotificationList
  },

  data() {
    return {
      msg: 'behold. my first Vue app',
      user: null,
      messages: {},
      form: {
        entity: 'warkatu'
      }
    }
  },

  mounted() {
    axios
      .get('http://127.0.0.1:5000/me')
      .then(response => {
        if (response.data.error) { throw response.data.error };
        this.user = response.data;
      })
      .catch (errorMessage => {
        this.addMessage('error', errorMessage);
        console.error(errorMessage);
      })
  },

  methods: {
    addMessage(type, text) {
      let _id = getUniqueId();
      // possibility of duplicate IDs is extremely low, though
      if (this.messages[_id]) _id = getUniqueId();
      if (!messageTypeAllowed.includes(type)) type = 'info';
      const message = {
        id: _id,
        type: type,
        text: text
      }
      // reactivity was learned the painful way
      this.$set(this.messages, _id, message);
    }
  }
}
</script>

<style lang="sass">
@import 'assets/variables'
@import 'assets/mixins'

html, body
  color: $main-light
  height: 100vh
  width: 100vw
  padding: 0
  margin: 0
  @include gradient($color1: $main-light, $color2: $main-dark)

.container
  margin: auto
  background: $bg-normal
  height: 100%
  width: 90vw
  max-width: 1140px

.content
  padding: 2rem

a
  color: $main-normal
</style>
