<template>
  <div class="spawner">
    <p>notification spawn tester ugly window</p>
    <form
      v-on:submit.prevent="onSubmit"
    >

      <div class="field">
        <textarea
          id="errorText"
          v-model="errorText"
          type="errorText"
          v-bind:class="{ 'danger': formError }"
        ></textarea>
      </div>

      <div class="field"
        v-if="formError">
        <span class='danger'>cannot send empty text</span>
      </div>


      <div class="field">
        <select v-model="errorType">
          <option selected>error</option>
          <option>info</option>
        </select>
        <input
          type="submit"
          value="SPAWN"
        >
      </div>

    </form>
  </div>
</template>

<script>
import eventBus from '../event-bus';

export default {
  data() {
    return {
      formError: false,
      errorText: 'print error message here',
      errorType: 'error',
    }
  },

  methods: {
    onSubmit: function() {
      this.formError = this.errorText ? false : true;
      eventBus.$emit(this.errorType, this.errorText);
    }
  }
}
</script>

<style lang="sass" scoped>
  @import '../assets/mixins'
  @import '../assets/variables'

  .danger
    color: $danger
    
  .spawner
    width: 100%
    max-width: 320px
    margin: 2rem
    padding-bottom: 4px
    background: $bg-dark
    color: $main-color
    font-size: .875rem
    border: 1px solid $main-dark

    p:first-child
      padding: 0 8px
      font-size: .65rem
      font-family: monospace

  textarea
    width: 100%
    min-height: 5rem
    background: darken($main-light, 10%)
    border: 2px solid transparent

    &:focus
      background: $main-light
      outline: none

  textarea.danger
    background: lighten($danger, 30%)
    border-color: $danger

  .field
    display: flex
    justify-content: space-between
    padding: 8px 8px

    input, select
      padding: 5px
      font-size: 1.2rem
      line-height: 1.2rem
      letter-spacing: 1px

      option:first-child
        background: lighten($danger, 15%)

      option:nth-child(2)
        background: $main-normal

</style>
