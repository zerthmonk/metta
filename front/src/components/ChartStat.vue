<template>
  <div>
    <zingchart
      :data="chartData"
    >

    </zingchart>
  </div>
</template>

<script>
import 'zingchart/es6';
import zingchartVue from 'zingchart-vue';

zingchart.THEME = 'dark';

export default {

  data() {
    return {
        chartData: {
            type: 'line',
            series: [{
                values: [4,5,3,3,4,4]
            }]
        }
    }
  },

  components: {
    zingchart: zingchartVue,
  }

}
</script>

<style lang="sass" scoped>

</style>
