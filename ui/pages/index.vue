<template lang="pug">
  main.vh-100.vw-100
    no-ssr
      heat-map(v-if="locationGot" :center="mapCenter", :zoom="mapZoom")

</template>
<script>
import HeatMap from '@/components/heatmap'

export default {
  components: {
    HeatMap
  },
  data () {
    return {
      mapCenter: [23.6068584,120.9653962],
      mapZoom: 8.25,
      locationGot: false,
    }
  },
  mounted () {
    this.updateLocation()
  },
  methods: {
    updateLocation () {
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(position => {
          this.mapCenter = [
            position.coords.latitude,
            position.coords.longitude
          ]
          this.mapZoom = 14
          this.locationGot = true
        }, () => {
          this.locationGot = true
        })
      } else {
        this.locationGot = true
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  .title {
    background: black;
    color: #fff;
  }
}
</style>
