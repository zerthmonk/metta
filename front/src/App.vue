<template>
  <div id="app" class="container">
    <div class="content">
      <UserStat
        :user="user"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UserStat from './components/UserStat.vue';

export default {
  name: 'app',
  components: {
		UserStat
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
  mounted() {
    axios
      .get('http://127.0.0.1:5000/me')
      .then(response => {
        this.user = response.data;
        console.log(this.user);
      })
  }
}
</script>

<style lang="sass">
@import 'assets/variables'

html, body
  color: $main-light
  background: $bg-dark
  height: 100vh
  width: 100vw
  padding: 0
  margin: 0

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
