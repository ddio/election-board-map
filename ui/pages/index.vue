<template lang="pug">
  main.vh-100.vw-100
    no-ssr
      heat-map(:center="mapCenter", :zoom="mapZoom")
    transition(name="fade")
      .absolute.absolute--fill.flex.items-center.justify-center.bg-black-30.z-9999(v-if="showGeoTips")
        .ba.bg-white.w6.tc.pa3
          h2.f3.mt3.mb4 嘿，想看看你附近有哪些看板嗎？
          .flex.justify-around
            button.ba.bg-near-white.w-40.pa3.pointer.hover-bg-light-gray(@click="showGeoTips = false")
              | 讓我自己逛逛
            button.ba.w-40.bg-green.white.pointer.hover-bg-dark-green(@click="getLocation")
              | 跳到我附近

</template>
<script>
import HeatMap from '@/components/heatmap'

export default {
  components: {
    HeatMap
  },
  data () {
    return {
      showGeoTips: false,
      mapCenter: [23.6068584,120.9653962],
      mapZoom: 8.25,
    }
  },
  mounted () {
    this.initLocation()
  },
  methods: {
    async checkGeoPermission () {
      if (!navigator.permissions) {
        return undefined
      }

      const result = await navigator.permissions.query({name:'geolocation'})
      // state can ge granted, prompt
      console.log('CHECK GEO', result)
      return result.state
    },
    async initLocation () {
      if (!("geolocation" in navigator)) {
        return
      }

      const geoPermission = await this.checkGeoPermission()

      if (geoPermission === 'granted') {
        this.getLocation()
      } else if (geoPermission === 'prompt') {
        setTimeout(() => {
          this.showGeoTips = true
        }, 500)
      }

    },
    getLocation () {
      this.showGeoTips = false
      navigator.geolocation.getCurrentPosition(position => {
        this.mapCenter = [
          position.coords.latitude,
          position.coords.longitude
        ]
        this.mapZoom = 14
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.button--primary {
  background: #f57c00;
  color: white;
}
</style>
<style lang="scss">
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>

