<template>
<form
  id="app"
  @submit="checkForm"
>

  <p v-if="errors.length">
    <b>Please correct the following error(s):</b>
    <ul>
      <li v-for="error in errors"
          :key=error.key>
          {{ error.text }}
      </li>
    </ul>
  </p>

  <p>
    <label for="entity">Entity name</label>
    <input
      id="entity"
      v-model="entity"
      type="text"
      name="entity"
    >
  </p>

  <p>
    <input
      type="submit"
      value="Submit"
    >
  </p>

</form>
</template>

<script>
import { BACKEND_URL } from '../conf';
import eventBus from '../event-bus';

export default {
  data() {
    return {
      errors: [],
      entity: '',
    }
  },

  methods: {
    checkForm: (e) => {
      if (this.entity && this.entity.length) {
        return true;
      }
      if (!this.entity) {
        this.errors.push({
          key: this.errors.length + 1,
          text: 'Entity name required.'
        });
      }
      e.preventDefault();
    }
  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/mixins'
  @import '../assets/variables'

</style>
