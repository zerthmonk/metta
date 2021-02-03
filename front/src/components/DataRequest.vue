<template>
  <div class='data-wrapper'>
    <div class="data-request">
      <form v-on:submit.prevent="checkForm">

        <p>
          <input
            id="entity"
            v-model="form.entity"
            type="text"
            name="entity"
          >
          <input
            type="submit"
            value="Search"
          >
        </p>
      </form>
    </div>
    <div class="data-response">
      <user-stat :user=user></user-stat>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL } from '../conf';
import eventBus from '../event-bus';

import UserStat from './UserStat.vue';

const infoUrl = `${BACKEND_URL}/info`;
const dataUrl = `${BACKEND_URL}/messages`;


export default {
  components: { UserStat },

  data() {
    return {
      stats: null,
      user: null,
      form: {
        entity: ''
      }
    }
  },

  methods: {

    checkForm() {
      // validation goes here
      if (this.form.entity != '') {
        this.getData(infoUrl, (user) => this.user = user);
        this.getData(dataUrl, (stats) => this.stats = stats);
      }
    },

    getData(url, setData) {
      axios.post(url, this.form)
        .then(response => {
          if (response.data.error) { throw response.data.error };
          eventBus.$emit('info', 'retrieving data...');
          setData(response.data);
        })
        .catch (errorMessage => {
          eventBus.$emit('error', errorMessage);
        })
    },

  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/mixins'
  @import '../assets/variables'

  .data-wrapper
    height: 10vh
    display: flex
    justify-content: space-between
    padding: .5rem 1.5rem

    div
      display: flex
      flex-direction: column
      justify-content: center


    .data-response
      display: flex
      max-width: 50%

    .data-request
      input
        padding: 1rem

</style>
