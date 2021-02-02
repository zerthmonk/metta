<template>
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

    <p>{{this.result}}</p>

  </form>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL } from '../conf';
import eventBus from '../event-bus';

const URL = `${BACKEND_URL}/info`;

export default {

  data() {
    return {
      result: '',
      form: {
        entity: ''
      }
    }
  },

  methods: {

    checkForm() {
      // validation goes here
      if (this.form.entity != '') {
        this.searchEntity();
      }
    },

    searchEntity() {
      console.log(`posting to ${URL}`);
      axios.post(`${URL}`, this.form)
        .then(response => {
          if (response.data.error) { throw response.data.error };
          eventBus.$emit('info', 'successful info request, retrieving data...')
          this.result = response.data;
        })
        .catch (errorMessage => {
          eventBus.$emit('error', errorMessage);
        })
    }
  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/mixins'
  @import '../assets/variables'

  form
    padding-left: 2rem

    input
      padding: 1rem

</style>
