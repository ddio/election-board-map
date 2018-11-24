<template lang="pug">
  section
    transition(name="fade")
      .absolute.absolute--fill.flex.items-center.justify-center.bg-black-30.z-9999(v-if="hasTipToShow")
        .bg-white.tc.pa3.br2.shadow-1(v-show="showGeoTips")
          h2.f3.mt3.mb4.normal 嘿，來看看附近有哪些看板？
          .flex.justify-around
            button.br2.ba.bg-near-white.w-50.pa3.pointer.hover-bg-light-gray(@click="showGeoTips = false")
              | 讓我自己逛逛
            button.br2.ba.w-40.bg-green.white.pointer.hover-bg-dark-green(@click="getLocation")
              | 跳到我附近
        .ba.bg-white.w5.tc.pa3(v-show="waitGeoInit")
          h2.f3.mv4 地圖定位中..

</template>
<script>
import { mapMutations } from 'vuex'

export default {
  data () {
    return {
      showGeoTips: false,
      waitGeoInit: false,
    }
  },
  computed: {
    hasTipToShow () {
      return this.showGeoTips || this.waitGeoInit
    }
  },
  mounted () {
    this.initLocation()
  },
  methods: {
    ...mapMutations(['centerMap', 'zoomMap']),
    async checkGeoPermission () {
      if (!navigator.permissions) {
        return undefined
      }

      const result = await navigator.permissions.query({name:'geolocation'})
      // state can ge granted, prompt
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
      this.waitGeoInit = true
      navigator.geolocation.getCurrentPosition(position => {
        this.centerMap([
          position.coords.latitude,
          position.coords.longitude
        ])
        this.zoomMap(14)
        setTimeout(() => {
          this.waitGeoInit = false
        }, 300)
      }, (err) => {
        if (err.code === 1) {
          alert('被拒絕了 T___T 請重開瀏覽器，或解除位置存取的封鎖')
        }
        this.waitGeoInit = false
      })
    }
  }
}
</script>

