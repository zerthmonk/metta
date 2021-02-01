<template>
  <div id="app" class="container">
    <div class="content user-content">
      <UserStat
        :user="user"
      />
    </div>
    <user-request></user-request>
    <error-spawner></error-spawner>
    <notification-list ref='notifications'></notification-list>
  </div>
</template>

<script>
import axios from 'axios';
import eventBus from './event-bus.js';
import { BACKEND_URL } from './conf';

import UserStat from './components/UserStat.vue';
import UserRequest from './components/UserRequest.vue';
import NotificationList from './components/NotificationList.vue';
import ErrorSpawner from './components/ErrorSpawner.vue';

console.log(`working with ${BACKEND_URL}`);


export default {
  name: 'app',
  components: {
    UserStat,
    UserRequest,
    NotificationList,
    ErrorSpawner
  },

  data() {
    return {
      msg: 'behold. my first Vue app',
      user: null,
      form: {
        entity: 'warkatu'
      }
    }
  },

  created() {
    eventBus.$on('error', (e) => this.$refs.notifications.addMessage('error', e));
    eventBus.$on('info', (e) => this.$refs.notifications.addMessage('info', e));
  },

  mounted() {
    this.getLoginInfo();
  },

  methods: {

    getLoginInfo() {
      axios.get(`${BACKEND_URL}/me`)
        .then(response => {
          if (response.data.error) { throw response.data.error };
          this.user = response.data;
        })
        .catch (errorMessage => {
          this.$refs.notifications.addMessage('error', errorMessage);
        })
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
  width: 100%
  max-width: 1140px

.content
  padding: 1.5rem

.user-content
  border-bottom: 1px solid lighten($bg-normal, 10%)

a
  color: $main-normal

</style>
